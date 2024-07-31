import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

# Input 
    # [Cluster1,Cluster2 , . . . ]

# Output 
    # [(1,2),(3,2),(4,5) ,  . . .]
    # [(cluster1, cluster2), (cluster, base station),  . . . ]
def createEdges(net):

        def cal_distance(point1, point2):
            return np.sqrt((point1[1]-point2[1])**2+(point1[2]-point2[2])**2)

        def list_nearest_centroid(centroid_x,centroid_y, list_centroid):
            sorted_points = sorted(list_centroid, key=lambda x: ((x[1] - centroid_x) ** 2 + (x[2] - centroid_y) ** 2) ** 0.5)
            closest_point_ids = [point[0] for point in sorted_points]
            return closest_point_ids
        
        def angle_between_points(point1, point2):
            A= np.array([point1[1],point1[2]])
            B= np.array([point2[1],point2[2]])
            C= np.array(net.baseStation.location)
            vector_AB = B - A
            vector_AC = C - A
            angle_BAC = np.arctan2(np.linalg.det([vector_AB, vector_AC]), np.dot(vector_AB, vector_AC))
            angle_BAC_deg = np.degrees(angle_BAC)
            return angle_BAC_deg

        list_id_centroid_cluster = []
        bs = [-1,500,500]
        edges = []
        edges_id = []
        list_common_elements = []
        para = len(net.listTargets)/5
        # print(para)
        # para = 10
        print(len(net.listTargets))

        for cluster in net.listClusters:
            list_id_centroid_cluster.append((cluster.id,cluster.centroid[0],cluster.centroid[1]))

        sorted_points = sorted(list_id_centroid_cluster, key=lambda point: cal_distance(point, bs), reverse=True)
        sorted_ids_distance = [point[0] for point in sorted_points]
        print("target",len(net.listTargets))
        print("target",net.listTargets)
        print("target")

        for point in sorted_points:
            list_angle_satisfy= []
            list_point_distance_satisfy = []
            sorted_nearest_point = list_nearest_centroid(point[1],point[2],list_id_centroid_cluster)

            for other_point in list_id_centroid_cluster:
                if point != other_point and angle_between_points(point,other_point)<= 45 and angle_between_points(point,other_point)>= -45:
                    list_angle_satisfy.append(other_point[0])

            for other_point in list_id_centroid_cluster:
                if point != other_point:
                    if cal_distance(point,other_point)< cal_distance(point,bs) and cal_distance(point,bs) > cal_distance(other_point,bs):
                        list_point_distance_satisfy.append(other_point[0])
            
            common_elements = []
            for id in sorted_nearest_point:
                if id in list_angle_satisfy and id in list_point_distance_satisfy:
                    common_elements.append(id)
            list_common_elements.append([point[0],common_elements])

        # Số target mà cụm phải tải ban đầu
        num_targets_clusters=[]
        for id in sorted_ids_distance:
            for cluster in net.listClusters:
                if id == cluster.id:
                    num_targets_clusters.append([cluster.id,len(cluster.listTargets)])
        
        print(num_targets_clusters)
        
        # Chọn cạnh
        print("Common point: ", list_common_elements)
        for point in list_common_elements:
            id =point[0]
            common_points = point[1]
            for targets_cluster1 in num_targets_clusters:
                if id == targets_cluster1[0]:
                    num_targets_point = targets_cluster1[1]
             
            if common_points:
                found = False
                for common_point in common_points:
                    for targets_cluster in num_targets_clusters:
                        if targets_cluster[0] == common_point:
                            if num_targets_point + targets_cluster[1] < para:
                                edges_id.append([id,common_point])
                                targets_cluster[1]=targets_cluster[1]+num_targets_point
                                found=True
                                break
                    if found:
                        break
                if not found:
                    edges_id.append([id,-1]) 
            else:
                for cluster in net.listClusters:
                    if cluster.id == id:
                        edges_id.append((id,-1))
        # for point in list_common_elements:
        #     id =point[0]
        #     common_points = point[1]
        #     for targets_cluster1 in num_targets_clusters:
        #         if id == targets_cluster1[0]:
        #             num_targets_point = targets_cluster1[1]
        #     if common_points: 
        #         for target_cluster in num_targets_clusters:
        #             if target_cluster[0]==common_points[0]:
        #                 edges_id.append([id,common_points[0]])
        #                 target_cluster[1]= target_cluster[1]+num_targets_point
        #                 if target_cluster[1]>= 40:
        #                     edges_id.append([id,-1])
        #                     target_cluster[1]=target_cluster[1]/2
        #     else:
        #         for cluster in net.listClusters:
        #             if cluster.id == id:
        #                 edges_id.append((id,-1))
            


        print("Số target tải mỗi cluster")
        print(num_targets_clusters)

        # for targets_cluster in num_targets_clusters:
        #     for edge in edges_id:
        #         if targets_cluster[0] == edge[1]:
        #             for add_targets in num_targets_clusters:
        #                 if add_targets[0] == edge[0]:
        #                     targets_cluster[1] = targets_cluster[1]+add_targets[1]
        #                     break
                    
        edges = []
        for edge in edges_id:
            for cluster in net.listClusters:
                if cluster.id == edge[0]:
                    cluster1 = cluster  
                if cluster.id == edge[1]:
                    cluster2 = cluster  
                if edge[1] == -1:
                    cluster2 = net.baseStation 
            edges.append((cluster1,cluster2))
         # Vẽ 
        edge_colors = cycle([ 'g', 'b', 'y', 'c', 'm', 'k'])

        cluster_colors = ['g', 'b', 'y', 'c', 'm', 'pink', 'orange', 'purple', 
                        'brown', 'olive', 'teal', 'navy', 'maroon', 'lime', 'aqua', 'fuchsia',
                        'indigo', 'gold']
        plt.figure(figsize=(10, 10))
        for i in range(len(net.listClusters)):
            cluster = net.listClusters[i]
            color = cluster_colors[i % len(cluster_colors)]  
            # Trích xuất các điểm và điểm centroid từ dữ liệu cluster
            points = [target.location for target in cluster.listTargets]
            centroid = cluster.centroid
            x_points = [point[0] for point in points]
            y_points = [point[1] for point in points]
            # Tạo mảng tọa độ x và y của điểm centroid
            centroid_x = centroid[0]
            centroid_y = centroid[1]
            # Vẽ các điểm trong cluster (trừ điểm centroid)
            plt.scatter(x_points, y_points, color=color)
            # Vẽ điểm centroid
            plt.scatter(centroid_x, centroid_y, color='red')
        # Vẽ các cạnh giữa các cluster
        for edge, color in zip(edges, edge_colors):

            if edge[1] is net.baseStation:
                x_values = [edge[0].centroid[0], 500]
                y_values = [edge[0].centroid[1], 500]
                plt.plot(x_values, y_values, color=color)
            else:
                # Trích xuất tọa độ của các điểm trong cạnh
                x_values = [edge[0].centroid[0], edge[1].centroid[0]]
                y_values = [edge[0].centroid[1], edge[1].centroid[1]]
                plt.plot(x_values, y_values, color=color)
        plt.scatter(500, 500, color='red', marker='*', s=300, label='Base Station')
        
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()
        return edges, num_targets_clusters
