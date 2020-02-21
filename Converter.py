from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsField
from PyQt5.QtCore import QVariant

def getSingleLines(layer):
    lines = []
    features = layer.getFeatures()
    for feature in features:
        geom = feature.geometry()
        if geom.isMultipart():
            multiLines = geom.asMultiPolyline()
            for line in multiLines:
                lines.append(line)
        else:
            line = geom.asPolyline()
            lines.append(line)
    return lines

def createPointLayer(points, name):
    pointLayer = QgsVectorLayer("Point?crs=epsg:3857", name, "memory")
    provider = pointLayer.dataProvider()
    provider.addAttributes([QgsField('type', QVariant.String)])
    pointLayer.updateFields()
    for point in points:
        feature = QgsFeature(pointLayer.fields())
        feature.setGeometry(QgsGeometry.fromPointXY(point[0]))
        feature.setAttribute('type', point[1])
        provider.addFeatures([feature])    
    return pointLayer

def convertToMemoryLayer(layer, type, outputName):
    features = [feature for feature in layer.getFeatures()]
    memoryLayer = QgsVectorLayer(type, outputName, "memory")
    memoryLayer_data = memoryLayer.dataProvider()
    attributes = layer.dataProvider().fields().toList()
    memoryLayer_data.addAttributes(attributes)
    memoryLayer.updateFields()
    memoryLayer_data.addFeatures(features)
    return memoryLayer

def polygonToPoints(feature):
    points = []
    geometry = feature.geometry();
    if geometry:
        if geometry.isMultipart():
            for singleGeometry in geometry.asMultiPolygon():
                verticesOuterRing = singleGeometry[0];
                for vertex in verticesOuterRing:
                    points.append(vertex)
        else:
            if (geometry.asPolygon()):
                verticesOuterRing = geometry.asPolygon()[0];
                for vertex in verticesOuterRing:
                    points.append(vertex)
    return points

def exportPolygons(layer, fileName, attributeIndex, numDecimalDigits):
    format = "%." + str(numDecimalDigits) + "f";
    iter = layer.getFeatures();
    f = open( fileName, 'wt');
    line = "";
    bbox = layer.extent();
    line = str(format % bbox.xMinimum()) + " " + str(format % bbox.yMinimum()) + " " + str(format % bbox.xMaximum()) + " " + str(format % bbox.yMaximum()) + "\n";
    f.write(line);
    line = "";
    
    for feature in iter:
        geometry = feature.geometry();
        if geometry:
            if geometry.isMultipart():
                for singleGeometry in geometry.asMultiPolygon():
                    verticesOuterRing= singleGeometry[0];
                    if (attributeIndex== -1):
                        attribute = "NONE";
                    else:
                        attribute = feature[attributeIndex];
                    line = "A " + str(attribute) + "\n";
                    for vertex in verticesOuterRing:
                        x = str(format % vertex.x());
                        y = str(format % vertex.y());
                        line = line + x + " " + y + "\n";
                    f.write(line);
            else:
                if (geometry.asPolygon()):
                    verticesOuterRing= geometry.asPolygon()[0];
                    if (attributeIndex== -1):
                        attribute = "NONE";
                    else:
                        attribute = feature[attributeIndex];
                    line = "A " + str(attribute) + "\n";
                    for vertex in verticesOuterRing:
                        x = str(format % vertex.x());
                        y = str(format % vertex.y());
                        line = line + x + " " + y + "\n";
                    f.write(line);
    f.close();

