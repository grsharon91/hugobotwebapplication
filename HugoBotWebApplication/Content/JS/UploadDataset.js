var myApp = angular.module('myApp', []);



myApp.directive('lettersNumbers', function () {
    return {
        require: '^ngModel',
        link: function (scope, element, attrs, model) {
            model.$validators.passwordPattern = function myValidation(value) {
                //var numbr = /\d/;
                //var letter = /[a-zA-Z]/;
                var lettersAndNumbers = /^[A-Za-z0-9]+$/;
                if (/**numbr.test(value) && letter.test(value) &&**/ lettersAndNumbers.test(value)) {
                    return true;
                } else {
                    return false;
                }
                //return value;
            };
        }
    };
});


myApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function () {
                scope.$apply(function () {
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);


myApp.service('fileUpload', ['$http', function ($http) {
    let self = this;
    self.numOfMapRows = 0;


    this.uploadFileToUrl = function (file, source, type,isPrivate, uploadUrl) {
        var fd = new FormData();
        if (isPrivate === undefined)
            isPrivate = false;
        fd.append('file', file);
        fd.append('source', source);
        fd.append('isPrivate', isPrivate);
        fd.append('type', type);
        return $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: { 'Content-Type': undefined }
        }).then(function (response) {
            return response.data;
        });


    };

    this.uploadMapFileFromPCToUrl = function (dataToSend, uploadUrl) {
        var fd = new FormData();
        fd.append('file', dataToSend);

        return $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: { 'Content-Type': undefined }
        }).then(function (response) {
            return response.data;
        });
    };

    this.uploadMapFileToUrl = function (dataToSend, uploadUrl) {
        return $http.post(uploadUrl, dataToSend, {
            transformRequest: angular.identity,
            headers: { 'Content-Type': undefined }
        }).then(function (response) {
            return response.data;
        });
    };


    this.uploadEntities = function (file, uploadUrl) {
        var fd = new FormData();
        fd.append('file', file);
        return $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: { 'Content-Type': undefined }
        }).then(function (response) {
            return response.data;
        });
    };

}]);

myApp.controller('myDatasetController', ['$scope', 'fileUpload', '$http', '$window', function ($scope, fileUpload, $http, $window) {
    showDatasetTab();
    clearUploadButton();
    let self = this;
    self.dicDuplicates = { Item1: [], Item2: [], Item3: [] };
    self.notMapped = [];
    self.showEntitiesFrom = false;
    self.showLoader = false;
    $scope.Map = {};
    $scope.currentMap = [];
    self.toShowErrors = false;
    self.toShowCorrupedRows = false;
    self.inconsistentDataShow = false;
    self.UploadMapFromPcShow = false;
    self.MapOptionsShow = false;
    self.userChoose = "";
    self.response = "";
    self.corruptedRowsDic = {};
    self.res = null;



    $scope.uploadEntitiesFile = function () {
        var file = $scope.myEntitiesFile;

        var uploadUrl = "/UploadDataset/UploadEntities";
        fileUpload.uploadEntities(file, uploadUrl)
            .then(function (res) {
                self.toShowEntitiesErrors = false;
                if (res === '0') {
                    self.toShowEntitiesErrors = true;
                    self.entitiesError = "Please upload a file."
                }else
                if (res === '1')
                {
                    self.toShowEntitiesErrors = true;
                    self.entitiesError = "Please upload a CSV file."
                } else
                if (res === '2') {
                    self.toShowEntitiesErrors = true;
                    self.entitiesError = "The first column doesn't contain only Int values for ID's, please fix it and upload the file again."
                        }
                if (res === '3')
                    window.location.pathname = '/Dataset/MyFiles';
            });

    };

    $scope.uploadFile = function () {

        self.showLoader = true;
        var file = $scope.myFile;

        console.log('file is ');
        console.dir(file);

        var uploadUrl = "/UploadDataset/UploadData";
        fileUpload.uploadFileToUrl(file, $scope.source, $scope.type, $scope.isPrivate, uploadUrl)
            .then(function (res) {
                self.toShowErrors = false;
                self.MapOptionsShow = false;
                self.UploadMapFromPcShow = false;
                self.UploadMapFromSiteShow = false;
                self.toShowCorrupedRows = false;
                self.inconsistentDataShow = false;
                if (res === '-3') {
                    self.MapOptionsShow = true;
                    self.showLoader = false;
                    showMapTab();
                }
                else if (res === "0") {
                    self.toShowErrors = true;
                    self.showLoader = false;
                    self.message = "Please upload a dataset."
                }
                else if (res === "-1") {
                    self.toShowErrors = true;
                    self.showLoader = false;
                    self.message = "Error! Please upload a CSV file.";
                }
                else if (res === "-2") {
                    self.toShowErrors = true;
                    self.showLoader = false;
                    self.message = "Error! File's header or colums are not in the right format.";

                }
                else if (res.charAt(0) === '1') {
                    self.showLoader = false;
                    let dicErrorTypes = angular.fromJson(res.substr(1));
                    self.toShowCorrupedRows = true;
                    self.corruptedRowsDic = dicErrorTypes;
                }
                else if (res.charAt(0) === '2') {
                    self.showLoader = false;
                    let dicInconsistentData = angular.fromJson(res.substr(1));
                    self.inconsistentDataShow = true;
                    self.inconsistentData = dicInconsistentData;

                }

            });

    };

    $scope.getTheMapChoose = function () {
        let choice = $scope.userChoose;

        if (choice === "1") {
            self.UploadMapFromPcShow = true;
            self.UploadMapFromSiteShow = false;

        } else if (choice === "2") {

            self.UploadMapFromPcShow = false;
            $scope.getMapValueFromDataset();
        }
    };




    $scope.getMapValueFromDataset = function () {
        let getArrResponse = [];
        self.uniqePropertyId = [];
        self.toShowErrors = false;
        $http.get('/UploadDataset/GetMapToEdit')
            .then(function (response) {

                $scope.currentMap = [];
                self.dicDuplicates.Item1 = [];
                self.dicDuplicates.Item2 = [];
                getArrResponse = angular.fromJson(response.data);
                self.uniqePropertyId = getArrResponse;
                fileUpload.numOfMapRows = getArrResponse.length;
                self.UploadMapFromSiteShow = true;

                for (let i = 0; i < fileUpload.numOfMapRows; i++) {
                    let dic = {
                        id: self.uniqePropertyId[i], name: "", description: "", error: [false, false, false]
                    };
                    $scope.currentMap.push(dic);
                }
                $scope.disableMap = true;



            });
    };
    $scope.Remove = function (index) {
        //Find the record using Index from Array.
        var id = $scope.currentMap[index].id;
        if ($window.confirm("Do you want to delete the property id: " + id)) {
            //Remove the item from Array using Index.
            $scope.currentMap.splice(index, 1);
            fileUpload.numOfMapRows--;
        }
    };
    $scope.Add = function () {
        //Add the new item to the Array.
        var property = {};
        property.id = $scope.id;
        property.name = $scope.name;
        property.description = $scope.description;
        $scope.id = "";
        $scope.name = "";
        $scope.description = "";
        fileUpload.numOfMapRows++;
        $scope.currentMap.push(property);
    };
    $scope.editAllMap = function () {
        $scope.disableMap = false;
    };

    $scope.disableEditMap = function () {
        $scope.disableMap = true;
    };



    $scope.uploadMapFileFromPC = function () {
        var file1 = $scope.myFileMap;
        var uploadUrl = "/UploadDataset/UploadMapFileFromPC";
        fileUpload.uploadMapFileFromPCToUrl(file1, uploadUrl)
            .then(function (res) {
                $scope.currentMap = [];
                self.dicDuplicates.Item1 = [];
                self.dicDuplicates.Item2 = [];
                $scope.disableMap = true;
                self.toShowErrors = false;
                self.UploadMapFromSiteShow = false;
                self.notMapped = [];
                if (res === "-1") {
                    self.toShowErrors = true;
                    self.messagMapError = "Please upload a dataset file first.";
                }
                else if (res === "0") {
                    self.toShowErrors = true;
                    self.messagMapError = "Please upload a map file.";
                }// if 0
                else if (res === "1") {
                    self.toShowErrors = true;
                    self.messagMapError = "Error! Please upload a CSV file.";
                }// if 1
                else if (res === "2") {
                    self.toShowErrors = true;
                    self.messagMapError = "Error! File's header or colums are not in the right format.";

                }// if 2
                else if (res.charAt(0) === '3') {
                    self.toShowErrors = true;
                    self.messagMapError ="The following cells have unvalid data types (printed in red):"
                    self.UploadMapFromSiteShow = true;
                    let dicErrorTypesMap = angular.fromJson(res.substr(1));
                    $scope.currentMap = [];

                    for (let i = 0; i < dicErrorTypesMap.Item2.length; i++) {
                        let dic = {
                            id: dicErrorTypesMap.Item2[i].temporalpropertyid, name: dicErrorTypesMap.Item2[i].temporalpropertyname, description: dicErrorTypesMap.Item2[i].description, error: [dicErrorTypesMap.Item1[i][0], dicErrorTypesMap.Item1[i][1], dicErrorTypesMap.Item1[i][2]]
                        };
                        $scope.currentMap.push(dic);
                    }
                    $scope.disableMap = false;
                }//if 1
                else if (res.charAt(0) === '4') {
                    self.UploadMapFromSiteShow = true;
                    self.toShowErrors = false;
                    self.dicDuplicates = angular.fromJson(res.substr(1));
                    $scope.currentMap = [];
                    for (let i = 0; i < self.dicDuplicates.Item3.length; i++) {
                        let dic = {
                            id: self.dicDuplicates.Item3[i].temporalpropertyid, name: self.dicDuplicates.Item3[i].temporalpropertyname, description: self.dicDuplicates.Item3[i].description, error: [false, false, false]
                        };
                        $scope.currentMap.push(dic);
                    }
                   
                }// if 4


            });
    };




    $scope.uploadMapFileFromSite = function () {
        var formToSend = new FormData();
        var formData = $scope.currentMap;
        for (let i = 1; i <= formData.length; i++) {
            if (formData[i - 1]["id"] === undefined)
                formData[i - 1]["id"] = "";
            if (formData[i - 1]["name"] === undefined)
                formData[i - 1]["name"] = "";
            if (formData[i - 1]["description"] === undefined)
                formData[i - 1]["description"] = "";
            formToSend.append("id" + i, formData[i - 1]["id"]);
            formToSend.append("name" + i, formData[i - 1]["name"]);
            formToSend.append("description" + i, formData[i - 1]["description"]);
        }

        var uploadUrl = "/UploadDataset/UploadMapFileFromSite";
        fileUpload.uploadMapFileToUrl(formToSend, uploadUrl)
            .then(function (res) {
                self.notMapped = [];
                self.dicDuplicates.Item1 = [];
                self.dicDuplicates.Item2 = [];
                self.toShowErrors = false;
                self.UploadMapFromSiteShow = false;
                for (let i = 0; i < $scope.currentMap.length; i++) {
                    $scope.currentMap[i].error[0] = false;
                    $scope.currentMap[i].error[1] = false;
                    $scope.currentMap[i].error[2] = false;
                }
                if (res === '-1') {
                    self.toShowErrors = true;
                    self.messagMapError = "Please upload a dataset file first.";
                }
                else if (res === '0') {
                    self.toShowErrors = true;
                    self.messagMapError = "Please upload a map file.";
                }// if 0
                else if (res.charAt(0) === '1') {
                    self.UploadMapFromSiteShow = true;
                    self.messagMapError = "The following cells have unvalid data types (printed in red):"
                    self.toShowErrors = true;
                    let dicErrorTypesMap = angular.fromJson(res.substr(1));
                    for (var key in dicErrorTypesMap) {
                        $scope.currentMap[key].error = dicErrorTypesMap[key];
                    }

                    $scope.disableMap = false;
                }// if 1
                else if (res.charAt(0) === '2') {
                    self.UploadMapFromSiteShow = true;
                    self.dicDuplicates = angular.fromJson(res.substr(1));
                    $scope.currentMap = [];
                    self.notMapped = [];
                    for (let i = 0; i < self.dicDuplicates.Item3.length; i++) {
                        let dic = {
                            id: self.dicDuplicates.Item3[i].temporalpropertyid, name: self.dicDuplicates.Item3[i].temporalpropertyname, description: self.dicDuplicates.Item3[i].description, error: [false, false, false]
                        };
                        $scope.currentMap.push(dic);

                    }
                    $scope.disableMap = false;
                }// if 2
                else if (res.charAt(0) === '3') {
                    self.UploadMapFromSiteShow = true;
                    self.notMapped = angular.fromJson(res.substr(1));
                    for (let i = 0; i < $scope.currentMap.length; i++) {
                        $scope.currentMap[i].error[0] = false;
                        $scope.currentMap[i].error[1] = false;
                        $scope.currentMap[i].error[2] = false;
                    }
                    $scope.disableMap = false;
                }//if 3
                else if (res.charAt(0) === '4') {
                    self.UploadMapFromSiteShow = true;
                    let propertiesID = "";
                    self.morePropertiesMapped = angular.fromJson(res.substr(1));
                    for (let i = 0; i < self.morePropertiesMapped.length; i++) {
                        propertiesID += self.morePropertiesMapped[i] + " ";
                    }
                    if ($window.confirm("The following Properties ID's are appearing in map file, but not in the dataset: " + propertiesID + "\nDo you want to remove them? ")) {
                        for (let i = 0; i < self.morePropertiesMapped.length; i++) {
                            let index = $scope.currentMap.indexOf(self.morePropertiesMapped[i]);
                            $scope.currentMap.splice(index, 1);
                        }

                    }
                    $http.get('/UploadDataset/sendToServerAfterConfirm')
                        .then(function (response) {
                            window.location.pathname = '/Dataset/MyFiles';
                        })
                }
                else if (res === '5') {
                    self.showEntitiesFrom = true;
                    showEntitiesTab();
                    
                }
            });
    };
}]);