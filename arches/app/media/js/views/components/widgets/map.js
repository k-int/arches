define([
    'underscore',
    'knockout',
    'knockout-mapping',
    'arches',
    'viewmodels/widget',
    'viewmodels/map-editor',
    'templates/views/components/widgets/map.htm',
    'templates/views/components/map-widget-editor.htm',
    'turf',
    'bindings/chosen',
    'bindings/codemirror',
    'select-woo',
    'bindings/fadeVisible',
    'bindings/mapbox-gl',
    'bindings/color-picker',
    'bindings/key-events-click',
], function (_, ko, koMapping, arches, WidgetViewModel, MapEditorViewModel, mapWidgetTemplate, mapWidgetEditorTemplate, turf) {
    var viewModel = function (params) {

        let self = this

        this.context = params.type;

        this.summaryDetails = [];
        this.defaultValueOptions = [
            {
                "name": "",
                "defaultOptionid": 0,
                "value": ""
            },
            {
                "name": "Drawn Location",
                "defaultOptionid": 1,
                "value": "Drawn Location"
            },
            {
                "name": "Current Device Location",
                "defaultOptionid": 2,
                "value": "Current Device Location"
            }
        ];

        params.configKeys = [
            'basemap',
            'overlayConfigs',
            'zoom',
            'centerX',
            'centerY',
            'geometryTypes',
            'defaultValueType',
            'defaultValue'
        ];

        WidgetViewModel.apply(this, [params]);

        this.geometryTypeList = ko.computed({
            read: function () {
                var geometryTypes = this.geometryTypes() || [];
                return geometryTypes.map(function (type) {
                    return ko.unwrap(type.id);
                });
            },
            write: function (value) {
                this.geometryTypes(value.map(function (type) {
                    return {
                        id: type,
                        text: type
                    };
                }));
            },
            owner: this
        });

        this.displayValue = ko.computed(function () {
            var value = koMapping.toJS(this.value);
            if (!value || !value.features) {
                return 0;
            }
            return value.features.length;
        }, this);

        if (params.widget) {
            params.widgets = [params.widget];
        }

        if (ko.unwrap(this.value) !== null) {
            this.summaryDetails = koMapping.toJS(this.value).features || [];
        }

        this.pointExpanded = ko.observable(false);
        this.lineStringExpanded = ko.observable(false);
        this.polygonExpanded = ko.observable(false);

        this.geometryTypeCounts = ko.computed(function () {
            let geometry_type_counts = {
                point: 0,
                lineString: 0,
                polygon: 0
            }

            this.summaryDetails.forEach(geometry => {
                let geometry_type = geometry["geometry"]["type"]
                geometry_type_counts[geometry_type[0].toLowerCase() + geometry_type.slice(1)] ++
            })

            return geometry_type_counts
        }, this)

        this.polygonBulletPoints = ko.computed(function () {
            let polygonBulletPoints = []

            this.summaryDetails.forEach(geometry => {
                if (geometry["geometry"]["type"] == "Polygon") {
                    const polygon = turf.polygon(geometry["geometry"]['coordinates']);
                    const centroid = turf.centroid(polygon)
                    const centroidCoords = centroid.geometry.coordinates.map(x => x.toFixed(4))
                    const polygonText = `Polygon ${polygonBulletPoints.length + 1}: [${centroidCoords[0]}, ${centroidCoords[1]}] (centre point)`
                    polygonBulletPoints.push(polygonText); 
                }
            })
            return polygonBulletPoints
        }, this)

        this.lineStringBulletPoints = ko.computed(function () {
            let lineStringBulletPoints = []

            this.summaryDetails.forEach(geometry => {
                if (geometry["geometry"]["type"] == "LineString") {
                    const lineString = turf.lineString(geometry["geometry"]['coordinates']);
                    const lineStringLength = turf.length(lineString, { units: 'kilometers' });
                    const lineStringMidpoint = turf.along(lineString, lineStringLength / 2, {units: 'kilometers'});
                    const midpointCoords = lineStringMidpoint.geometry.coordinates.map(x => x.toFixed(4));
                    const lineStringText = `LineString ${lineStringBulletPoints.length + 1}: [${midpointCoords[0]}, ${midpointCoords[1]}] (mid-point)`
                    lineStringBulletPoints.push(lineStringText); 
                }
            })
            return lineStringBulletPoints
        }, this)

        this.pointBulletPoints = ko.computed(function () {
            let pointBulletPoints = []

            this.summaryDetails.forEach(geometry => {
                if (geometry["geometry"]["type"] == "Point") {
                    let pointCoordinates = geometry["geometry"]['coordinates'].map(x => x.toFixed(4))
                    const pointText = `Point ${pointBulletPoints.length + 1}: [${pointCoordinates[0]}, ${pointCoordinates[1]}]`
                    pointBulletPoints.push(pointText); 
                }
            })
            return pointBulletPoints
        }, this)

        this.showCopyText = ko.observable(false);

        this.copyGeoJSON = function() {
            self.showCopyText(true);
            console.log(this.showCopyText())
            window.setTimeout(function(){
                self.showCopyText(false);
                console.log(self.showCopyText())
            }, 6000);
        }

        if (this.centerX() == 0 && this.centerY() == 0 && this.zoom() == 0) {
            this.centerX(arches.mapDefaultX);
            this.centerY(arches.mapDefaultY);
            this.zoom(arches.mapDefaultZoom);
        }

        params.basemap = this.basemap;
        params.overlayConfigs = this.overlayConfigs;
        params.zoom = this.zoom;
        params.x = this.centerX;
        params.y = this.centerY;
        params.usePosition = true;
        params.inWidget = true;

        MapEditorViewModel.apply(this, [params]);

    };

    ko.components.register('map-widget', {
        viewModel: viewModel,
        template: mapWidgetTemplate,
    });

    return viewModel;
});
