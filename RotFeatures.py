import pandas as pd
import pygplates
import numpy as np
import os


'''csv_filename, 
encoding_type='utf-8', 
rotation_file = 'PALEOMAP_PlateModel.rot', 
static_polygons = 'PALEOMAP_PlatePolygons.gpml
默认编码方式utf-8, 旋转模型文件和静态多边形文件是Scotese, 2016
可以通过指定rotation_file, static_polygons自定义模型文件和多边形文件
'''


def rot(csv_filename,
        encoding_type='utf-8',
        rotation_file='PALEOMAP_PlateModel.rot',
        static_polygons='PALEOMAP_PlatePolygons.gpml'):
    # 旋转模型文件和静态多边形文件，默认使用Scotese, 2016的模型
    rotation_model = pygplates.RotationModel(rotation_file)

    output_points = 'output_points.gpml'  # tmp file, removed at the end

    df = pd.read_csv(csv_filename, encoding=encoding_type, low_memory=False)

    filtered_df = df.dropna(subset=['lng', 'lat'])

    # 判断 reconstruction_age 列是否存在且非空
    if 'reconstruction_age' in filtered_df.columns and filtered_df['reconstruction_age'].notnull().all():
        # 如果 reconstruction_age 列存在且非空，则将其赋值给 age_mid 变量
        age_mid = np.squeeze(np.array(filtered_df['reconstruction_age']))
    else:
        # 获取age中值，通过 最小年龄：min_ma，最大年龄：max_ma计算
        age_min = np.squeeze(np.array(filtered_df['reconstruction_age']))
        age_max = np.squeeze(np.array(filtered_df['reconstruction_age']))
        age_mid = (age_min + age_max) / 2.

    # 记录点的数量
    n_points = len(age_mid)

    # 获取lon, lat
    lon = np.squeeze(np.array(filtered_df['lng'])) if 'lng' in filtered_df.columns else np.squeeze(
        np.array(filtered_df['lon']))
    lat = np.squeeze(np.array(filtered_df['lat']))

    # 旋转模型文件和静态多边形文件，默认使用Scotese, 2016的模型
    rotation_model = pygplates.RotationModel('PALEOMAP_PlateModel.rot')
    static_polygons = 'PALEOMAP_PlatePolygons.gpml'
    output_points = 'output_points.gpml'  # tmp file, removed at the end

    input_points = []
    for i in np.arange(n_points):  # n_points (replace with e.g. 10000 to test script on a subset of data)
        # Create a pyGPlates point from the latitude and longitude, and add it to our list of points.
        input_points.append(pygplates.PointOnSphere(lat[i], lon[i]))

    # Create a feature for each point we read from the input file.
    point_features = []
    for point in input_points:
        # Create an unclassified feature.
        point_feature = pygplates.Feature()
        # Set the feature's geometry to the input point read from the text file.
        point_feature.set_geometry(point)
        point_features.append(point_feature)

    # Use the static polygons to assign plate IDs and valid time periods.
    # Each point feature is partitioned into one of the static polygons and assigned its
    # reconstruction plate ID and valid time period.
    assigned_point_features = pygplates.partition_into_plates(
        static_polygons,
        rotation_model,
        point_features,
        properties_to_copy=[
            pygplates.PartitionProperty.reconstruction_plate_id,
            pygplates.PartitionProperty.valid_time_period])

    output_points = 'output_points.gpmlz'
    assigned_point_feature_collection = pygplates.FeatureCollection(assigned_point_features)
    assigned_point_feature_collection.write(output_points)

    # Restore points to a geological time based on rotation model

    features = pygplates.FeatureCollection(output_points)
    # print(output_points)

    # 对数据流进行扩列
    filtered_df['paleolon'] = pd.Series(dtype='float64')
    filtered_df['paleolat'] = pd.Series(dtype='float64')
    # 用于存放古经纬度的数组
    paleolat = np.full((n_points), np.nan)
    paleolon = np.full((n_points), np.nan)

    counter = 0
    for feature in features:
        reconstruction_time = age_mid[counter]
        paleocoords = []  # possibility to use a list or a string (to save to file)
        pygplates.reconstruct(feature, rotation_model, paleocoords, reconstruction_time)
        if len(paleocoords) > 0:  # some data points disappear because of rotational model
            # https://www.gplates.org/docs/pygplates/pygplates_reference.html#geometry
            # https://www.gplates.org/docs/pygplates/generated/pygplates.reconstructedfeaturegeometry
            # paleocoords[0].get_present_day_geometry().to_lat_lon_list()
            paleolat[counter] = paleocoords[0].get_reconstructed_geometry().to_lat_lon_list()[0][0]
            paleolon[counter] = paleocoords[0].get_reconstructed_geometry().to_lat_lon_list()[0][1]
        else:
            paleolat[counter] = np.nan
            paleolon[counter] = np.nan
        counter += 1

    filtered_df['paleolon'] = paleolon
    filtered_df['paleolat'] = paleolat

    # removing rows with no data
    n_noNA = filtered_df['paleolon'].isnull().sum()
    # PBDB_table_noNA = filtered_df.dropna(axis=0, how = 'any', inplace=False)
    # n_droppedrows = n_points - len(PBDB_table_noNA)
    percent_droppedrows = np.around((n_noNA) / n_points * 100., 1)
    print(str(int(n_noNA)) + '/' + str(int(n_points))
          + ' (' + str(percent_droppedrows) + '%) cannot complete the rotation.')

    # writing to csv
    outname = csv_filename[:-4] + '_rotatedScotese2016.csv'
    filtered_df.to_csv(outname, sep=',', encoding='utf-8')
    print('Saving to file: ' + outname)


if __name__ == '__main__':
    csv_filename = 'simple.csv'  # 在此填入你的csv文件名 , 注意要跟该本文文件处在同一个目录中
    # 新文件命名为simple_rotatedScotese2016.csv
    rot(csv_filename)  # 编码方式，不填写的话默认为 utf-8
