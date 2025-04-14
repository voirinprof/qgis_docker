from flask import Flask, Response, request, jsonify
import os
from qgis.core import QgsProject, QgsVectorLayer, QgsMapSettings, QgsRectangle
import requests

app = Flask(__name__)
DATA_DIR = '/data'  # shared volume with QGIS Server
QGIS_SERVER_URL = 'http://nginx:80/ows/'  # internal URL of QGIS Server

@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.json
    project_name = data.get('name', 'new_project')
    shapefile = data.get('shapefile', 'world.shp')

    # path of the project
    project_path = os.path.join(DATA_DIR, f"{project_name}.qgs")
    # path of the shapefile
    shapefile_path = os.path.join(DATA_DIR, shapefile)

    # create a new QGIS project
    project = QgsProject.instance()
    project.clear()

    # add a new layer
    # you should adapt according to your shapefile
    layer = QgsVectorLayer(shapefile_path, "Countries", "ogr")
    if not layer.isValid():
        return jsonify({"error": "Invalid shapefile"}), 400
    project.addMapLayer(layer)

    # save the project
    project.write(project_path)
    return jsonify({"message": f"Project {project_name} created", "path": project_path}), 201

# list all projects
@app.route('/list_projects', methods=['GET'])
def list_projects():
    projects = [f for f in os.listdir(DATA_DIR) if f.endswith('.qgs')]
    return jsonify({"projects": projects})

# use qgis server to render the map
@app.route('/map/<project_name>', methods=['GET'])
def get_map(project_name):
    project_path = os.path.join(DATA_DIR, f"{project_name}.qgs")
    if not os.path.exists(project_path):
        return jsonify({"error": f"Project not found {project_path}"}), 404

    # call QGIS Server to render the map
    params = {
        'SERVICE': 'WMS',
        'REQUEST': 'GetMap',
        'VERSION': '1.3.0',
        'MAP': f"/io/data/{project_name}.qgs",
        'LAYERS': 'Countries',
        'STYLES': '',
        'CRS': 'EPSG:4326',
        'WIDTH': '800',
        'HEIGHT': '600',
        'FORMAT': 'image/png',
        'BBOX': '-180,-90,180,90'  
    }
    response = requests.get(QGIS_SERVER_URL, params=params)
    
    if response.status_code != 200:
        return jsonify({"error": f"Failed to render map {response.url}"}), 500

    return Response(response.content, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)