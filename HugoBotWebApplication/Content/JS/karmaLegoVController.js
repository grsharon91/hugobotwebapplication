myApp.directive('onFinishRender', function ($timeout) {
    return {
        restrict: 'A',
        link: function (scope, element, attr) {
            if (scope.$last === true) {
                $timeout(function () {
                    scope.$emit('ngRepeatFinished');
                });
            }
        }
    };
});
myApp.directive('sglclick', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function (scope, element, attr) {
            var fn = $parse(attr['sglclick']);
            var delay = 300, clicks = 0, timer = null;
            element.on('click', function (event) {
                clicks++;  //count clicks
                if (clicks === 1) {
                    timer = setTimeout(function () {
                        scope.$apply(function () {
                            fn(scope, { $event: event });
                        });
                        clicks = 0;             //after action performed, reset counter
                    }, delay);
                } else {
                    clearTimeout(timer);    //prevent single-click action
                    clicks = 0;             //after action performed, reset counter
                }
            });
        }
    };
}]);






myApp.controller('KarmalegoVcontroller', ['$scope', '$http', function ($scope, $http) {
    vm = this;
    vm.metadata = [];
    vm.curResult = []; // contain only what was in the WPF in RootElement 
    vm.relationDic = { "<": "Before", "=": "Equals", "m": "Meet", "c": "Contains", "s": "Starts", "f": "Finishes", "o": "Overlaps", "X": "No relation" };
    vm.propertiesColors = [];


    ///////shows///////////////

    vm.showInformationTable1 = false;
    vm.showInformationTable2 = false;
    vm.showCurrentLevel = false;
    /////////end shows///////////


    vm.rootProperties = [];
    //vm.rootProperties.push({ "StateID": 1, "relation": "X.", "vertical": 1993 });
    //vm.rootProperties.push({ "StateID": 4, "relation": "X.", "vertical": 1733 });
    //vm.rootProperties.push({ "StateID": 5, "relation": "X.", "vertical": 1620 });
    //vm.rootProperties.push({ "StateID": 6, "relation": "X.", "vertical": 1636 });
    //vm.rootProperties.push({ "StateID": 41, "relation": "X.", "vertical": 1670 });
    //vm.rootProperties.push({ "StateID": 42, "relation": "X.", "vertical": 1708 });
    //vm.rootProperties.push({ "StateID": 48, "relation": "X.", "vertical": 1858 });
    //vm.rootProperties.push({ "StateID": 49, "relation": "X.", "vertical": 1970 });
    //vm.rootProperties.push({ "StateID": 50, "relation": "X.", "vertical": 1906 });
    //vm.rootProperties.push({ "StateID": 51, "relation": "X.", "vertical": 1804 });
    //vm.rootProperties.push({ "StateID": 54, "relation": "X.", "vertical": 1959 });
    //vm.rootProperties.push({ "StateID": 55, "relation": "X.", "vertical": 1975 });
    //vm.rootProperties.push({ "StateID": 56, "relation": "X.", "vertical": 1970 });
    //vm.rootProperties.push({ "StateID": 61, "relation": "X.", "vertical": 1997 });
    //vm.rootProperties.push({ "StateID": 62, "relation": "X.", "vertical": 1993 });
    //vm.rootProperties.push({ "StateID": 63, "relation": "X.", "vertical": 1993 });
    //vm.rootProperties.push({ "StateID": 65, "relation": "X.", "vertical": 1993 });
    //vm.rootProperties.push({ "StateID": 67, "relation": "X.", "vertical": 1993 });
    //vm.rootProperties.push({ "StateID": 69, "relation": "X.", "vertical": 1993 });
    //vm.rootProperties.push({ "StateID": 74, "relation": "X.", "vertical": 1993 });
    //vm.rootProperties.push({ "StateID": 75, "relation": "X.", "vertical": 1993 });
    ////     vm.rootProperties.push({ "StateID": 76, "relation": "X.", "vertical": 1993 });
    //vm.rootProperties.push({ "StateID": 2, "relation": "X.", "vertical": 1993 });


    /* ALON 17_Jun */
    vm.loadFiles = function () {
        $http.post('/KarmaLegoV/loadFiles')
            .then(function (response) {
                $http.get('/KarmaLegoV/getMetadata')
                    .then(function (res) {
                        vm.metadata = res.data;
                        vm.rootProperties = vm.metadata.index;
                        vm.setTheRootElements();
                        vm.entitiesColums = [];
                        for (col in vm.metadata.datEntities[0]) {
                            vm.entitiesColums.push(col);
                        }
                        vm.entitiesDetailsToById();
                        vm.setColorsToStates();

                    });

            });
    };

    vm.loadFiles();


    vm.entitiesDetailsToById = function () {
        vm.entitiesDetailsByID = {};
        for (let i = 0; i < vm.metadata.datEntities.length; i++) {
            let entityDet = {};
            for (let j = 0; j < vm.entitiesColums.length; j++) {
                entityDet[vm.entitiesColums[j]] = vm.metadata.datEntities[i][vm.entitiesColums[j]];
            }
            vm.entitiesDetailsByID[vm.metadata.datEntities[i][vm.entitiesColums[0]]] = entityDet;
        }
    };
    vm.getRootElements = function (stateID) {

        /*$http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: { 'Content-Type': undefined }
        })*/
        var fd = new FormData();

        let propertyName = vm.metadata.dictState[stateID];
        fd.append('propertyName', propertyName);
        fd.append('isMerged', 'false');
        $http.post('/KarmaLegoV/getSubTree', fd, {
            transformRequest: angular.identity,
            headers: { 'Content-Type': undefined }
        }).then(function (response) {
                vm.curResult = response.data;
                //vm.setTheRootElements();


                // vm.nextElementsList = vm.curResult.RootElements.PropertiesList[0].NextLevel.PropertiesList;
                vm.nextElementsList = vm.curResult.PropertiesList;

                vm.numOfNextState = vm.nextElementsList.length;
                vm.nextLevelStatesNames = [];
                for (i = 0; i < vm.numOfNextState; i++) {
                    vm.nextLevelStatesNames.push({
                        "stateID": vm.nextElementsList[i].StateID,
                        "stateName": vm.metadata.dictState[vm.nextElementsList[i].StateID],
                        "relation": vm.nextElementsList[i].Relations[vm.nextElementsList[i].Relations.length - 2],
                        "vertical": vm.nextElementsList[i].VerticalSupport,
                        "localHorz": vm.nextElementsList[i].HorizontalSupport / vm.nextElementsList[i].VerticalSupport
                        //"globalHorz": vm.nextElementsList[i].HorizontalSupport / vm.metadata.datEntities.length
                    });
                }
            });
    };

    vm.getRootNextLevel = function (stateID) {
        var fd = new FormData();

        let propertyName = vm.metadata.dictState[stateID];
        fd.append('propertyName', propertyName);
        fd.append('isMerged', 'false');
        $http.post('/KarmaLegoV/getSubTree', fd, {
            transformRequest: angular.identity,
            headers: { 'Content-Type': undefined }
        }).then(function (response) {
                /* ALON: try to remove root element
                vm.curResult = response.data;
                vm.curResult.RootElements.PropertiesList[0].StateID = stateID;
                vm.curResult.RootElements.PropertiesList[0].Relations = "X.";
                vm.currentElementsList = vm.curResult.RootElements.PropertiesList[0].NextLevel.PropertiesList;
                let index = vm.rootProperties.findIndex(state => state.StateID === stateID);
                vm.metadata.cutPropertiesPath.push(vm.curResult.RootElements.PropertiesList[0]);
                */
           
            vm.curResult = angular.fromJson(response.data);

                //vm.curResult.PropertiesList[0].StateID = stateID;
                //vm.curResult.PropertiesList[0].Relations = "X.";
          
            vm.currentElementsList = vm.curResult.PropertiesList;
            let temp = { "NextLevel": { "PropertiesList": vm.curResult.PropertiesList }, "StateID": stateID }; 
                let index = vm.rootProperties.findIndex(state => state.StateID === stateID);
            vm.metadata.cutPropertiesPath.push(temp);

                vm.fillCurrentLevelTable();
                vm.showInformationTable1 = false;
                vm.showCurrentLevel = true;
                vm.treeLevel++;
                vm.fillInformationTable2(0);

                vm.singleClick(vm.currentElementsList[0].StateID,0);
                vm.showStatistics = true;
                vm.showInstances = true;
                vm.treePath.push({
                    "treeLevel": vm.treeLevel,
                    "stateID": vm.metadata.cutPropertiesPath[vm.treeLevel - 1].StateID,
                    "stateName": vm.metadata.dictState[vm.metadata.cutPropertiesPath[vm.treeLevel - 1].StateID]
                });


            });
    };


    vm.rootSingleClick = function (stateID) {
        vm.getRootElements(stateID);


    };


    vm.rootDoubleClick = function (stateID) {
        vm.getRootNextLevel(stateID);
    };


    vm.setTheRootElements = function () {
        vm.showStatistics = false;
        vm.showInstances = false;
        vm.showInformationTable2 = false;
        vm.showCurrentLevel = false;
        vm.showInformationTable1 = true;
        //   vm.currentElementsList = vm.curResult.RootElements.PropertiesList;
        vm.currentNumOfStates = vm.rootProperties.length;
        vm.rootStatesNames = [];
        vm.currentInstances = [];
        vm.selectedInfo = [];
        vm.isChosenRow = [];
        for (i = 0; i < vm.currentNumOfStates; i++) {
            vm.rootStatesNames.push({
                "stateID": vm.rootProperties[i].StateID,
                "stateName": vm.metadata.dictState[vm.rootProperties[i].StateID],
                "vertical": vm.rootProperties[i].vertical,
                "relation": vm.rootProperties[i].relation[vm.rootProperties[i].relation.length - 2]
            });
        }
        let canvasContain = document.getElementById("canvasContainer");
        while (canvasContain.hasChildNodes()) {
            canvasContain.removeChild(canvasContain.lastChild);
        }
        vm.nextLevelStatesNames = [];
        vm.metadata.cutPropertiesPath = [];
        vm.currentStatesNames = [];
        vm.currentInstances = [];

        vm.treeLevel = 0;
        vm.showCanvas = false;
        vm.treePath = [];
        vm.treePath.push({ "treeLevel": vm.treeLevel, "stateID": -1, "stateName": "Root" });
        //vm.fillInstancesTable(0);
        let table = document.getElementById("relationTable");
        for (let m = table.rows.length; m > 0; m--) {
            table.deleteRow(m - 1);
        }
        vm.relationsID = [];
    };










    vm.fillInformationTable2 = function (i) {
        if (vm.treeLevel !== 0) {
            vm.information = {};
            vm.information =
                {
                    "TIV": vm.currentElementsList[i].TIV,
                    "vertSupport": vm.currentElementsList[i].VerticalSupport,
                    "localHorzSupport": vm.currentElementsList[i].HorizontalSupport / vm.currentElementsList[i].VerticalSupport,
                    "globalHorzSupport": vm.currentElementsList[i].HorizontalSupport / vm.metadata.datEntities.length,
                    "maxDepth": vm.currentElementsList[i].depth,
                    "numOfInstances": vm.currentElementsList[i].Instances.Instances.length,
                    "numOfStatesInNextLevel": vm.currentElementsList[i].NextLevel.PropertiesList.length
                };

            vm.showInformationTable1 = false;
            vm.showInformationTable2 = true;

        }
    };



    vm.Remove = function (index) {
        vm.entitiesDetails.splice(index, 1);
    };

    vm.singleClick = function (stateID,index) {

        if (vm.treeLevel === 0) {
            vm.rootSingleClick(stateID);
            let index = vm.rootStatesNames.findIndex(state => state.stateID === stateID);
            vm.setChosenRowColor(index);
        }
        else {
            //let index = vm.currentElementsList.findIndex(state => state.StateID === stateID);
            vm.nextElementsList = vm.currentElementsList[index].NextLevel.PropertiesList;

            vm.setChosenRowColor(index);
            if (vm.treeLevel !== 0) {
                vm.currentInstances = vm.currentElementsList[index].Instances;
                vm.findMaxEndPoint();
                vm.currentEntitiesID = [];
                for (let i = 0; i < vm.currentInstances.Instances.length; i++) {
                    //if (vm.currentEntitiesID.indexOf(vm.currentInstances.Instances[i].EntityID) === -1) {
                    vm.currentEntitiesID.push(vm.currentInstances.Instances[i].EntityID);

                    // }
                }
                vm.drawAVGStatesOnCanvas(index);
                vm.setTheCurrentRelations(index);
                vm.relationId(index);
                vm.buildRelationsTable();
                vm.showCanvas = true;
            }
            let canvasContain = document.getElementById("canvasContainer");
            while (canvasContain.hasChildNodes()) {
                canvasContain.removeChild(canvasContain.lastChild);
            }
            while (pieContainer.hasChildNodes()) {
                pieContainer.removeChild(pieContainer.lastChild);
            }
            vm.numOfNextState = vm.nextElementsList.length;
            vm.nextLevelStatesNames = [];
            for (i = 0; i < vm.numOfNextState; i++) {
                vm.nextLevelStatesNames.push({
                    "stateID": vm.nextElementsList[i].StateID,
                    "stateName": vm.metadata.dictState[vm.nextElementsList[i].StateID],
                    "relation": vm.nextElementsList[i].Relations[vm.nextElementsList[i].Relations.length - 2],
                    "vertical": vm.nextElementsList[i].VerticalSupport,
                    "localHorz": vm.nextElementsList[i].HorizontalSupport / vm.nextElementsList[i].VerticalSupport
                    //"globalHorz": vm.nextElementsList[i].HorizontalSupport / vm.metadata.datEntities.length
                });
            }
            if (vm.treeLevel !== 0) {
                vm.fillInformationTable2(index);
            }
        }

    };

    vm.doubleClick = function (stateID,index) {
        if (vm.treeLevel === 0) {
            if (vm.metadata.chunkesLargerThanZero.includes(vm.metadata.dictState[stateID]))
            {
                vm.rootDoubleClick(stateID);
            }
        }
        else {
           // let index = vm.currentElementsList.findIndex(state => state.StateID === stateID);
            if (vm.currentElementsList[index].NextLevel.PropertiesList.length !== 0) {
                vm.metadata.cutPropertiesPath.push(vm.currentElementsList[index]);
                vm.currentElementsList = vm.currentElementsList[index].NextLevel.PropertiesList;

                vm.fillCurrentLevelTable();


                vm.showInformationTable1 = false;
                vm.showCurrentLevel = true;
                vm.fillInformationTable2(0);
                vm.singleClick(vm.currentElementsList[0].StateID,0);
                vm.treeLevel++;
                vm.treePath.push({
                    "treeLevel": vm.treeLevel,
                    "stateID": vm.metadata.cutPropertiesPath[vm.treeLevel - 1].StateID,
                    "stateName": vm.metadata.dictState[vm.metadata.cutPropertiesPath[vm.treeLevel - 1].StateID]
                });
            }
        }

    };



    vm.path_Click = function (index) {
        if (index === 0) {
            vm.setTheRootElements();
            vm.currrentRelation = [];
        } else {
            vm.treeLevel = index;
            vm.currentElementsList = vm.metadata.cutPropertiesPath[vm.treeLevel - 1].NextLevel.PropertiesList;
            let canvasContain = document.getElementById("canvasContainer");
            while (canvasContain.hasChildNodes()) {
                canvasContain.removeChild(canvasContain.lastChild);
            }
            vm.metadata.cutPropertiesPath = vm.metadata.cutPropertiesPath.slice(0, vm.treeLevel);

            vm.treePath = vm.treePath.slice(0, vm.treeLevel + 1);
            vm.fillCurrentLevelTable();
            vm.fillInformationTable2(0);
            vm.singleClick(vm.currentElementsList[0].StateID,0);
        }


    };

    vm.fillCurrentLevelTable = function () {
        vm.currentNumOfStates = vm.currentElementsList.length;
        vm.currentStatesNames = [];
        for (i = 0; i < vm.currentNumOfStates; i++) {
            vm.currentStatesNames.push({
                "stateID": vm.currentElementsList[i].StateID,
                "stateName": vm.metadata.dictState[vm.currentElementsList[i].StateID],
                "relation": vm.currentElementsList[i].Relations[vm.currentElementsList[i].Relations.length - 2],
                "vertical": vm.currentElementsList[i].VerticalSupport,
                "localHorz": vm.currentElementsList[i].HorizontalSupport / vm.currentElementsList[i].VerticalSupport,
                "globalHorz": vm.currentElementsList[i].HorizontalSupport / vm.metadata.datEntities.length,
               

            });
        }
    };




    //vm.printAvg = function (stateID)
    //{
    //    KarmaService.instances = vm.currentInstances;
    //    KarmaService.changeData();
    //}



    function getRandomColor() {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }


    vm.drawCanvasAxis = function (canvas, ctx) {
        let maximunPoint = vm.maxPoint;
        let numOfTicks = Math.ceil(maximunPoint / 10);
        // canvas width
        let canvas_width = canvas.width;
        // canvas height
        let canvas_height = canvas.height;
        let margins = 25;
        vm.grid_size = (canvas.width - margins) / numOfTicks;
        let x_axis_distance_grid_lines = 1;
        let y_axis_distance_grid_lines = 1;
        let x_axis_starting_point = { number: 1 };


        let num_lines_y = Math.ceil(canvas_width / vm.grid_size);

        //print x-axis
        ctx.beginPath();
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#000000";
        ctx.moveTo(margins, margins * 6 - margins - 8);
        ctx.lineTo(canvas_width, margins * 6 - margins - 8);
        //ctx.moveTo(0, vm.grid_size * num_lines_x - vm.grid_size  );
        // ctx.lineTo(canvas_width, vm.grid_size * num_lines_x - vm.grid_size );
        ctx.stroke();

        //print y-axis
        ctx.beginPath();
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#000000";
        ctx.moveTo(margins, margins);
        ctx.lineTo(margins, canvas_height - 15);
        ctx.stroke();


        // Ticks marks along the positive X-axis
        for (i = 1; i < (num_lines_y - y_axis_distance_grid_lines); i++) {
            ctx.beginPath();
            ctx.lineWidth = 1;
            ctx.strokeStyle = "#000000";

            // Draw a tick mark 6px long (-3 to 3)
            ctx.moveTo(margins + vm.grid_size * i + 0.5, margins * 6 - margins - 11);
            ctx.lineTo(margins + vm.grid_size * i + 0.5, margins * 6 - margins + -5);
            ctx.stroke();

            // Text value at that point
            ctx.font = '9px Arial';
            ctx.textAlign = 'start';
            ctx.fillText(x_axis_starting_point.number * i * 10, margins + vm.grid_size * i - 2, margins * 6 - margins + 3);

        }
        ctx.font = '15px Roboto';
        ctx.textAlign = 'start';
        ctx.fillText("Time", 300, margins * 6 - margins + 18);
    };


    vm.drawAVGStatesOnCanvas = function (index) {
        let margins = 25;
        let canvas = document.getElementById('avgCanvas');
        let ctx = canvas.getContext("2d");
        // canvas width
        let canvas_width = canvas.width;
        // canvas height
        let canvas_height = canvas.height;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        vm.drawCanvasAxis(canvas, ctx);


        let numOfIntrervals = vm.currentInstances.lstAvgIntervals.length;
        let yAxisUnits = (canvas_height - margins * 2) / numOfIntrervals;
        let xAxisUnits = vm.grid_size / 10;
        vm.intervals = [];
        let count = 0;
        for (let z = 0; z < numOfIntrervals - 1; z++) {
            count++;
            vm.intervals.push({
                 "propertyName": vm.metadata.dictState[vm.metadata.cutPropertiesPath[z].StateID],
                //"propertyName": vm.metadata.dictState[vm.metadata.cutPropertiesPath[0][z].StateID],
                "startPoint": vm.currentInstances.lstAvgIntervals[z].StartTime,
                "endPoint": vm.currentInstances.lstAvgIntervals[z].EndTime
            });
        }
        vm.intervals.push({
            "propertyName": vm.metadata.dictState[vm.currentElementsList[index].StateID],
            "startPoint": vm.currentInstances.lstAvgIntervals[count].StartTime,
            "endPoint": vm.currentInstances.lstAvgIntervals[count].EndTime
        });
        ctx.font = '15px Roboto';
        ctx.textAlign = 'start';
        ctx.fillText("Average Pattern", (6 * 40), 20);
        for (let i = 1; i <= numOfIntrervals; i++) {

            ctx.beginPath();
            ctx.lineWidth = 6;
            let indexInColors = vm.propertiesColors.findIndex(prop => prop.stateName === vm.intervals[i - 1].propertyName);
            ctx.strokeStyle = vm.propertiesColors[indexInColors].color;
            ctx.moveTo(margins + (vm.intervals[i - 1].startPoint * xAxisUnits), yAxisUnits * i);
            ctx.lineTo(margins + (vm.intervals[i - 1].endPoint * xAxisUnits), yAxisUnits * i);
            ctx.stroke();
        }
    };


    vm.ClickInstanceAddCanvas = function (index) {
        var canvas = document.createElement('canvas');
        canvas.width = 600;
        canvas.height = 150;
        var ctx = canvas.getContext('2d');
        let margins = 25;
        canvas.style.backgroundColor = "white";
        //ctx.beginPath();
        //ctx.rect(0, 0, canvas.width, canvas.height);
        //ctx.fillStyle = "white";
        //ctx.fill();
        vm.drawCanvasAxis(canvas, ctx);

        // canvas width
        let canvas_width = canvas.width;

        // canvas height
        let canvas_height = canvas.height;


        ///////// start draw//////
        let instance = vm.currentInstances.Instances[index];
        let yAxisUnits = (canvas_height - margins * 2) / instance.Intervals.length;
        let xAxisUnits = vm.grid_size / 10;
        for (let i = 1; i <= instance.Intervals.length; i++) {
            ctx.beginPath();
            ctx.lineWidth = 6;
            let indexInColors = vm.propertiesColors.findIndex(prop => prop.stateName === vm.intervals[i - 1].propertyName);
            ctx.strokeStyle = vm.propertiesColors[indexInColors].color;
            ctx.moveTo(margins + (instance.Intervals[i - 1].StartTime * xAxisUnits), yAxisUnits * i);
            ctx.lineTo(margins + (instance.Intervals[i - 1].EndTime * xAxisUnits), yAxisUnits * i);
            ctx.stroke();
        }
        ctx.font = '15px Roboto';
        ctx.textAlign = 'start';
        ctx.fillText("ID : " + instance.EntityID, (6 * 50), 20);
        ctx.font = '30px Roboto';
        ctx.textAlign = 'start';
        ctx.fillText("x", 50 * 11 + margins, 20);

        var element = document.getElementById('canvasContainer');
        element.appendChild(canvas);

        canvas.addEventListener('click', function (event) {
            var rect = canvas.getBoundingClientRect();
            var x = event.clientX - rect.left,
                y = event.clientY - rect.top;
            // Collision detection between clicked offset and element.

            if (y > 0 && y < 20 && x > 50 * 11 + margins && x < 600) {
                element.removeChild(canvas);
            }


        }, false);
    };








    vm.setColorsToStates = function () {
        for (state in vm.metadata.dictState) {
            let color = getRandomColor();
            vm.propertiesColors.push({ "stateName": vm.metadata.dictState[state], "color": color });
        }
    };

    vm.relationId = function (index) {
        vm.relationsID = [];
        for (let i = 0; i < vm.metadata.cutPropertiesPath.length; i++) {
            vm.relationsID.push(vm.metadata.cutPropertiesPath[i].StateID);
        }
        vm.relationsID.push(vm.currentElementsList[index].StateID);
    };

    vm.buildRelationsTable = function () {
        let table = document.getElementById("relationTable");
        for (let m = table.rows.length; m > 0; m--) {
            table.deleteRow(m - 1);
        }
        let row = table.insertRow(0);
        let cell1 = row.insertCell(0);
        cell1.innerHTML = "";
        let index = vm.currentElementsList.findIndex(elem => elem.StateID === vm.relationsID[vm.relationsID.length - 1]);
        let lengthOfRelation = vm.currentElementsList[index].Relations.length;
        let count = 0;
        let count2 = 0;
        for (let i = 1; i < vm.relationsID.length; i++) {
            let cell2 = row.insertCell(i);
            cell2.innerHTML = vm.relationsID[i];
        }

        for (let j = 1; j < vm.relationsID.length; j++) {
            let row1 = table.insertRow(j);

            for (let k = 0; k < vm.relationsID.length; k++) {
                let cell3 = row1.insertCell(k);
                if (k === 0) {
                    cell3.innerHTML = vm.relationsID[count2];
                    count2++;
                }

                else if (k < j) {
                    cell3.innerHTML = "";
                }
                else {

                    cell3.innerHTML = vm.currentElementsList[index].Relations[count];
                    count = count + 2;
                }
            }
        }

    };


    vm.setTheCurrentRelations = function (index) {
        if (vm.metadata.cutPropertiesPath.length > 0) {

            vm.currrentRelation = [];
            for (let i = 0; i < vm.metadata.cutPropertiesPath.length; i++) {
                propery = vm.metadata.cutPropertiesPath[i];
                let indexInColors = vm.propertiesColors.findIndex(prop => prop.stateName === vm.metadata.dictState[propery.StateID]);
                vm.currrentRelation.push({ "propertyName": vm.metadata.dictState[propery.StateID], "propertyColor": vm.propertiesColors[indexInColors].color });
                //vm.currrentRelation.push({ "propertyName": vm.relationDic[propery.NextLevel.PropertiesList[index].Relations[propery.NextLevel.PropertiesList[index].Relations.length - 2]], "propertyColor": "transparent" });
            }
            let indexInColors2 = vm.propertiesColors.findIndex(prop => prop.stateName === vm.metadata.dictState[vm.currentElementsList[index].StateID]);
            vm.currrentRelation.push({ "propertyName": vm.metadata.dictState[vm.currentElementsList[index].StateID], "propertyColor": vm.propertiesColors[indexInColors2].color });
        }

    };




    vm.dropDownSelect = function () {
        let selected = vm.selected;
        vm.selectedInfo = {};
        for (let i = 0; i < vm.currentEntitiesID.length; i++) {
            let index = vm.metadata.datEntities.findIndex(ent => ent.id === vm.currentEntitiesID[i]);
            let value = vm.metadata.datEntities[index][selected];
            if (value in vm.selectedInfo) {
                vm.selectedInfo[value]++;
            } else {
                vm.selectedInfo[value] = 1;
            }
        }
        let keys = [];
        let values = [];
        let colors = [];
        for (key in vm.selectedInfo) {
            keys.push(key);
            values.push(vm.selectedInfo[key]);
            colors.push(getRandomColor());
        }
        var data = {
            labels: keys,
            datasets: [
                {
                    label: selected,
                    data: values,
                    backgroundColor: colors,
                    //borderColor: [
                    //    "#CDA776",
                    //    "#989898",
                    //    "#CB252B",
                    //    "#E39371",
                    //    "#1D7A46"
                    //],
                    borderWidth: [1, 1, 1, 1, 1]
                }
            ]
        };
        var pieContainer = document.getElementById('pieContainer');
        while (pieContainer.hasChildNodes()) {
            pieContainer.removeChild(pieContainer.lastChild);
        }
        // var canvas = document.getElementById('pieCanvas');
        var pieCanvas = document.createElement('canvas');
        pieCanvas.width = 275;
        pieCanvas.height = 125;




        pieContainer.appendChild(pieCanvas);
        var ctx = pieCanvas.getContext('2d');
        //ctx.style.backgroundColor = "white";


        window.myPie = new Chart(ctx, {
            type: 'pie',
            data: data,// init data, not from entities csv

            options: {
                tooltips: {
                    callbacks: {
                        label: function (tooltipItem, data) {
                            //var label = data.datasets[tooltipItem.datasetIndex].label || '';
                            let sum = 0;
                            for (let i = 0; i < data.datasets[tooltipItem.datasetIndex].data.length; i++) {
                                sum += data.datasets[tooltipItem.datasetIndex].data[i];
                            }
                            let percent = (data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] / sum) * 100;
                            percent = percent.toFixed(2);
                            var label = data.labels[tooltipItem.index] + ": " + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] + " (" + percent + "%)";
                            //if (label) {
                            //    label += ': ';
                            //}
                            //label += Math.round(tooltipItem.yLabel * 100) / 100;
                            return label;
                        }
                    }



                },
                responsive: false
            }
        });

        //updateData(keys, values, colors);
        pieContainer.appendChild(pieCanvas);
    };


    vm.setChosenRowColor = function (index) {
        vm.isChosenRow = [];
        for (let i = 0; i < vm.currentNumOfStates; i++) {
            if (i === index) {
                vm.isChosenRow[i] = true;
            }
            else
                vm.isChosenRow[i] = false;
        }
    };



    function updateData(keys, values, colors) {
        window.myPie.data.labels = [];
        window.myPie.data.labels = window.myPie.data.labels.concat(keys);

        window.myPie.data.datasets.forEach((dataset) => {
            dataset.data = [];
            dataset.data = dataset.data.concat(values);
        });
        window.myPie.update();
    }

    vm.findMaxEndPoint = function () {
        vm.maxPoint = 0;
        for (let i = 0; i < vm.currentInstances.Instances.length; i++) {
            if (vm.maxPoint < vm.currentInstances.Instances[i].maxPoint) {
                vm.maxPoint = vm.currentInstances.Instances[i].maxPoint;
            }

        }
    };




    $scope.$on('ngRepeatFinished', function (ngRepeatFinishedEvent) {
        for (let i = 0; i < vm.currentInstances.Instances.length; i++) {
            let canvasCreate = document.getElementById('canvas' + i);
            let canvas = canvasCreate.getContext("2d");
            canvas.width = 150;
            canvas.height = 25;
            let oneUnit = 150 / vm.maxPoint;
            canvas.moveTo(vm.currentInstances.Instances[i].minPoint * oneUnit, 15);
            canvas.lineTo(vm.currentInstances.Instances[i].maxPoint * oneUnit, 15);
            canvas.stroke();
        }
    });


    Chart.defaults.global.customTooltips = function (tooltip) {
        // Tooltip Element
        var tooltipEl = $('#chartjs-tooltip');
        // Hide if no tooltip
        if (!tooltip) {
            tooltipEl.css({
                opacity: 0
            });
            return;
        }
        // Set caret Position
        tooltipEl.removeClass('above below');
        tooltipEl.addClass(tooltip.yAlign);
        // Set Text
        tooltipEl.html(tooltip.text);
        // Find Y Location on page
        var top;
        if (tooltip.yAlign === 'above') {
            top = tooltip.y - tooltip.caretHeight - tooltip.caretPadding;
        } else {
            top = tooltip.y + tooltip.caretHeight + tooltip.caretPadding;
        }
        // Display, position, and set styles for font
        tooltipEl.css({
            opacity: 1,
            left: tooltip.chart.canvas.offsetLeft + tooltip.x + 'px',
            top: tooltip.chart.canvas.offsetTop + top + 'px',
            fontFamily: tooltip.fontFamily,
            fontSize: tooltip.fontSize,
            fontStyle: tooltip.fontStyle
        });
    };
}]);


///////////////////////////////////////////////////////////

//app.controller("DoughnutCtrl", function ($scope) {
//    $scope.labels = ["Download Sales", "In-Store Sales", "Mail-Order Sales"];
//    $scope.data = [300, 500, 100];
//    $scope.changeData = function () {
//        $scope.data = [100, 400, 500];
//    }
//});
