#!/usr/bin/env python3

#!/usr/bin/env python3

import time
import cv2
import depthai as dai
import open3d as o3d
import argparse

import pandas as pd

from .box_estimator_app  import BoxEstimator
from .projector_3d_app import PointCloudFromRGBD
import warnings

warnings.simplefilter("ignore")


#parser = argparse.ArgumentParser()
#parser.add_argument('-maxd', '--max_dist', type=float, help="Maximum distance between camera and object in space in meters",
#                    default=1.5)
#parser.add_argument('-mins', '--min_box_size', type=float, help="Minimum box size in cubic meters",
#                    default=0.003)

#args = parser.parse_args()

COLOR = True

lrcheck  = True   # Mejor manejo de las oclusiones
extended = False  # Más cerca de la profundidad mínima, el rango de disparidad se duplica
subpixel = False   # Mayor precisión para distancias más largas, disparidad fraccionaria 32 niveles
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7
median   = dai.StereoDepthProperties.MedianFilter.KERNEL_7x7

#print("StereoDepth config options:")
#print("    Left-Right check:  ", lrcheck)
#print("    Extended disparity:", extended)
#print("    Subpixel:          ", subpixel)
#print("    Median filtering:  ", median)

pipeline = dai.Pipeline()

monoLeft = pipeline.create(dai.node.MonoCamera)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)

monoRight = pipeline.create(dai.node.MonoCamera)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

stereo = pipeline.createStereoDepth()
stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_ACCURACY)
stereo.initialConfig.setMedianFilter(median)
stereo.setLeftRightCheck(lrcheck)
stereo.setExtendedDisparity(extended)
stereo.setSubpixel(subpixel)
monoLeft.out.link(stereo.left)
monoRight.out.link(stereo.right)

config = stereo.initialConfig.get()
config.postProcessing.speckleFilter.enable = False
config.postProcessing.speckleFilter.speckleRange = 50
config.postProcessing.temporalFilter.enable = False
config.postProcessing.spatialFilter.enable = True
config.postProcessing.spatialFilter.holeFillingRadius = 2
config.postProcessing.spatialFilter.numIterations = 1
config.postProcessing.thresholdFilter.minRange = 40
config.postProcessing.thresholdFilter.maxRange = 1500
config.postProcessing.decimationFilter.decimationFactor = 3
stereo.initialConfig.set(config)

xout_depth = pipeline.createXLinkOut()
xout_depth.setStreamName('depth')
stereo.depth.link(xout_depth.input)

# xout_disparity = pipeline.createXLinkOut()
# xout_disparity.setStreamName('disparity')
# stereo.disparity.link(xout_disparity.input)

xout_colorize = pipeline.createXLinkOut()
xout_colorize.setStreamName('colorize')
if COLOR:
    camRgb = pipeline.create(dai.node.ColorCamera)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
    camRgb.setIspScale(1, 3)
    #camRgb.setPreviewSize(300, 300)
    #.setPreviewSize(1920, 1080)
    camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
    #camRgb.initialControl.setManualFocus(230)
    stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
    camRgb.isp.link(xout_colorize.input)
else:
    stereo.rectifiedRight.link(xout_colorize.input)


class HostSync:
    def __init__(self):
        self.arrays = {}
    def add_msg(self, name, msg):
        if not name in self.arrays:
            self.arrays[name] = []
        # Agregar mensaje a la matriz
        self.arrays[name].append({'msg': msg, 'seq': msg.getSequenceNum()})

        synced = {}
        for name, arr in self.arrays.items():
            for i, obj in enumerate(arr):
                if msg.getSequenceNum() == obj['seq']:
                    synced[name] = obj['msg']
                    break
        # Si hay 3 (todos) mensajes sincronizados, elimine todos los mensajes antiguos
        # y devolver mensajes sincronizados
        if len(synced) == 2: # color, depth, nn
            # Eliminar mensajes antiguos
            for name, arr in self.arrays.items():
                for i, obj in enumerate(arr):
                    if obj['seq'] < msg.getSequenceNum():
                        arr.remove(obj)
                    else: break
            return synced
        return False
p=0
#n=0
list_dimeniones = []
consolo = []
with dai.Device(pipeline) as device:
    #for i in range(0, 10, 1):
    device.setIrLaserDotProjectorBrightness(1200)
    qs = []
    qs.append(device.getOutputQueue("depth", 1))
    qs.append(device.getOutputQueue("colorize", 1))
    calibData = device.readCalibration()
    if COLOR:
        w, h = camRgb.getIspSize()
        intrinsics = calibData.getCameraIntrinsics(dai.CameraBoardSocket.RGB, dai.Size2f(w, h))
        #print('Right mono camera focal length in pixels:', intrinsics[0][0])
    else:
        w, h = monoRight.getResolutionSize()
        intrinsics = calibData.getCameraIntrinsics(dai.CameraBoardSocket.RIGHT, dai.Size2f(w, h))
    # Duerme durante 5 segundos, para que la cámara se calme.
    time.sleep(2)
    pcl_converter = PointCloudFromRGBD(intrinsics, w, h)
    sync = HostSync()
    box_estimator = BoxEstimator(1.5)
    #print("primer while "+str(p))
    #i = 0
    t = time.time()
    while True:
        for p in range(10):
            #print("segundo while "+str(p))
            for q in qs:
                #print("for q " + str(p))
                new_msg = q.tryGet()
                if new_msg is not None:
                    msgs = sync.add_msg(q.getName(), new_msg)
                    if msgs:
                        #print("for msgs "+ str(p))
                        depth = msgs["depth"].getFrame()
                        color = msgs["colorize"].getCvFrame()
                        #cv2.imshow("The Forest Software Lab [Imagen Real]", color)
                        cv2.imwrite(
                            '/Users/javilizama/Desktop/HD/cubiScan/imagenes' + '/color5.jpg',
                            color)
                        #cv2.imwrite(
                        #    '/Users/javilizama/Desktop/HD/cubiScan/imagenes' + '/depth5.jpg',
                        #    depth)
                        rgb = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
                        pointcloud = pcl_converter.rgbd_to_projection(depth, rgb)
                        t_new = time.time()
                        dt =  t_new - t
                        fps = 1 / dt
                        t = t_new
                        l, w, h = box_estimator.process_pcl(pointcloud)
                        if(l * w * h  > 0.003):
                            #box_estimator.vizualise_box()
                            img = box_estimator.vizualise_box_2d(intrinsics, color)
                            #cv2.imshow("The Forest Software Lab [Proyeccion 2D]", img)
                            #print(f"Longitud: {l*100:.2f}, Ancho: {w*100:.2f}, Altura:{h*100:.2f}, i:{p:.2f}")
                            list_dimeniones.append(box_estimator.process_pcl(pointcloud))
                            #consolo=pd.DataFrame(box_estimator.process_pcl(pointcloud))
                            #cv2.imwrite(
                            #    '/Users/javilizama/Desktop/box_measurement/Test/api_dimensiones_img/img' + '/img4'+'_'+str(p)+'.png',
                            #    img)
                            p=p+1
                consolo=pd.DataFrame(list_dimeniones,columns=['Longitud','Ancho','Altura'])
#i=i+1
        if len(consolo)>=30:
            break
        #else:
        #    break
        #if cv2.waitKey(5) == ord('q'):
        #    break
        #elif cv2.waitKey(5)  == ord('s'):
            #o3d.io.write_triangle_mesh('/Users/javilizama/Desktop/jl_hd_oak/dimensionador_hd/box_measurement/api'+ '\img.png', pointcloud)
            #cv2.imwrite('/Users/javilizama/Desktop/jl_hd_oak/dimensionador_hd/box_measurement/api' + '\img.ply', rgb)
        #    print("image saved!")

def dimens():
    consolidado_final=[]
    m=0
    for m in range(0, len(consolo)):
        #consolo.loc[m, 'Longitud'] = consolo.loc[m, 'Longitud'] *100
        #consolo.loc[m, 'Ancho'] = consolo.loc[m, 'Ancho'] * 100
        #consolo.loc[m, 'Altura'] = consolo.loc[m, 'Altura'] * 100
        consolo.loc[m, 'Volumen'] = consolo.loc[m, 'Longitud'] * consolo.loc[m, 'Ancho'] * consolo.loc[m, 'Altura']
        mediana = consolo['Volumen'].median()
        mediana_LONG = consolo['Longitud'].median()
        mediana_ALTU = consolo['Altura'].median()
        mediana_ANCHO = consolo['Ancho'].median()


    consolidado_final={"largo":round(mediana_LONG*100,0),"ancho":round(mediana_ANCHO*100,0),"altura":round(mediana_ALTU*100,0)}
    #consolidado_final = pd.DataFrame(consolidado_final)
    return consolidado_final
#dimen = dimens()