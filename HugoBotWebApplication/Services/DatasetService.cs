using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Web;
using GenericParsing;
using HugoBotWebApplication.CommunicationLayer;
using HugoBotWebApplication.Models;
using HugoBotWebApplication.Models.Formats_Handling;
using HugoBotWebApplication.Models.Repositories;
using HugoBotWebApplication.Utils.FileHandlers;
using HugoBotWebApplication.ViewModels;
using Microsoft.AspNet.Identity;

namespace HugoBotWebApplication.Services
{
    public class DatasetService
    {
        private Dataset discretization;
        private readonly List<string> methodFullnames;
        private static ApplicationDbContext db = new ApplicationDbContext();
        private readonly DatasetRepository datasetRepository;
        private Dictionary<string, string> methodEncodingToMethodName = new Dictionary<string, string>()
                {
                    {"EQW", "Equal Width" },
                    {"EQF", "Equal Frequency" },
                    {"PERSIST", "Persist" },
                    {"EXPERT", "Expert" },
                    {"KMEANS", "Kmeans" },
                    {"BINARY", "Binary" },
                    {"TD4C", "TD4C" },
                    {"KARMALEGO", "KarmaLego"}
                    //{"$TD4C_Entropy", "TD4C_Entropy" },
                    //{"$TD4C_Cosine", "TD4C_Cosine" },
                    //{"$TD4C_KullbackLiebler", "TD4C_KullbackLiebler" },

                };
        private List<string> methodsWithParameters = new List<string> { "TD4C" };
        private IFileHandler<Measurement> datasetFileHandler = new DatasetFileHandler();
        private IFileHandler<VariableMetadata> metadataFileHandler = new MetadataFileHandler();
        public Dataset Discretization { get => discretization; set => discretization = value; }
        private FileTransferrer fileTransferrer = new FileTransferrer();
        private object memoryStream;

        public DatasetService(DatasetRepository datasetRepository)
        {
            this.datasetRepository = datasetRepository;
        }
        public DatasetService(Dataset discretization)
        {
            this.discretization = discretization;
        }

        public List<string> GetMethodsFullNames()
        {
            return methodFullnames;
        }
        private List<string> SetMethodsFullnames()
        {
            List<string> methodFullNames = new List<string>();
            foreach (var param in discretization.Parameters.Split(';'))
            {
                methodFullNames.Add(param.Split('$')[0]);
            }
            return methodFullNames;
        }
        private string FormatParams(string methodName, List<string> methodParameters)
        {
            string formattedParams = methodEncodingToMethodName[methodName] + "$" + methodName;
            foreach (var methodParam in methodParameters)
            {
                formattedParams = formattedParams + "_" + methodParam;
            }
            return ";" + formattedParams;
        }

        private int HasClass(List <string> temporalPropertyID)
        {
            var ans = 0;
            foreach (var id in temporalPropertyID)
            {
                int i=Int32.Parse(id);
                if (i < 0)
                    ans = 1;
            }
                return ans;
        }

        public byte[] GetDatasetFile(Dataset dataset)
        {
            FileTransferrer fileTransferrer = new FileTransferrer();
            byte[] datasetFile = fileTransferrer.GetFilesFromServer(dataset.Path);
            return datasetFile;
        }


        public byte[] GetEntitiesFile(Dataset dataset)
        {
            FileTransferrer fileTransferrer = new FileTransferrer();
            byte [] entitiesFile = fileTransferrer.GetFilesFromServer(dataset.EntitiesPath);
            return entitiesFile;
        }

        public  byte [] GetMetadataFile(Dataset dataset)
        {
            FileTransferrer fileTransferrer = new FileTransferrer();
            byte[] vmapFile = fileTransferrer.GetFilesFromServer(dataset.VmapPath);
            return vmapFile;
        }

        public byte[] GetAllFiles(Dataset dataset)
        {
            FileTransferrer fileTransferrer = new FileTransferrer();

            byte[] allFiles = fileTransferrer.GetFilesFromServer(dataset.Path + " " + dataset.VmapPath + " " + dataset.EntitiesPath);
            return allFiles;
        }

        public Dataset CreateDatasetFromDatasetViewModel(DatasetViewModel datasetViewModel,int datasetId, string datasetPath, string vmapPath,ApplicationUser currentUser, byte [] metadata)
        {
            return new Dataset()
            {
                DatasetName = datasetViewModel.DatasetName,
                Category = datasetViewModel.Category,
                Parameters = "",
                ParametersIsReady = "Ready",
                Path = datasetPath,
                VmapPath = vmapPath,
                Owner = currentUser,
                Visibility = datasetViewModel.Visibility,
                Rating = 0,
                Type = "Raw",
                Description = datasetViewModel.DatasetDescription,
                DatasetID = datasetId,
                NumberOfDownloads = 0,
                NumberOfViews = 0,
                DateUploaded = DateTime.Now,
                EntitiesPath = datasetPath + "/Entities",
                hasClass = HasClass(datasetViewModel.TemporalPropertyID),
                metaData = metadata

        };
        }

        public DatasetDetailsViewModel CreateDatasetDetailsViewModel(Dataset dataset)
        {
            //VariableMetadata[] metadata = metadataFileHandler.ReadFileToArray(dataset.VmapPath); 
            VariableMetadata[] metadata = metadataFileHandler.ReadBytesToArray(dataset.metaData);
            DatasetDetailsViewModel datasetDetailsViewModel = new DatasetDetailsViewModel()
            {
                DatasetID = dataset.DatasetID,
                DatasetName = dataset.DatasetName,
                Category = dataset.Category,
                VmapPath = dataset.VmapPath,
                Owner = dataset.Owner,
                Description = dataset.Description,
                Metadata = metadata,
                Dataset = dataset
            };
            return datasetDetailsViewModel;
        }


        public byte[] CreateMetadataFile(List<string> temporalPropertyIds, List<string> temporalPropertyNames, List<string> description)
        {
            //string currentUserId = User.Identity.GetUserId();
            int propertiesCount = temporalPropertyIds.Count;
            var variableMetadata = new VariableMetadata[propertiesCount];

            for (int i = 0; i < propertiesCount; i++)
            {
                variableMetadata[i] = new VariableMetadata()
                {
                    TemporalPropertyID = Int32.Parse(temporalPropertyIds[i]),
                    TemporalPropertyName = temporalPropertyNames[i],
                    Description = description[i]
                };
            }

            byte[] metadataFileBytes = metadataFileHandler.GetBytesFromArray(variableMetadata); 
            
            return metadataFileBytes;
        }


        //public string UploadDatasetFiles(string datasetName, HttpPostedFileBase datasetFile, byte[] metadataFileBytes, HttpPostedFileBase entitiesFile)
        //{
        //    //string datasetPath = fileTransferrer.SendDatasetFiles(datasetName, fileTransferrer.GetBytesFromFile(datasetFile), metadataFileBytes);
        //    //fileTransferrer.SendEntitiesFile(datasetPath, fileTransferrer.GetBytesFromFile(entitiesFile));
        //    //return datasetPath;
        //    DateTime date = DateTime.Now;
        //    string datasetPath = "~/App_Data/uploads/" + datasetFile.FileName.Substring(0, datasetFile.FileName.Length - 4) + "_" +
        //                 date.ToString("yyyy_MM_dd_H_mm_ss") + "/" + datasetFile.FileName;
        //    return datasetPath;
        //}

          public string getPath(string fileName, string date)
        {
            string path = "~/App_Data/uploads/" + fileName.Substring(0, fileName.Length - 4) + "_" +
                        date + "/" + fileName;
            return path;
        }

        public object CreateMetadataFileFromDatasetFile(HttpPostedFileBase datasetFile)
        {
            Measurement[] datasetArray = datasetFileHandler.ReadHttpPostedFileBaseToArray(datasetFile);
            int [] datasetPropertiesArray = GetPropertiesIdsFromDatasetFileArray(datasetArray).ToArray();
            List<VariableMetadata> vmapToSend = new List<VariableMetadata>();

            for (int i = 0; i < datasetPropertiesArray.Length; i++)
            {
                vmapToSend.Add(new VariableMetadata()
                {
                    TemporalPropertyID = datasetPropertiesArray[i],
                    TemporalPropertyName = "",
                    Description = "",
                });
            }
            var vmapErrors = new string[vmapToSend.Count];
            var vmapDatasetErrors = new string[datasetPropertiesArray.Length];
            for (int i = 0; i < vmapErrors.Length; i++)
                vmapErrors[i] = "";

            for (int i = 0; i < vmapDatasetErrors.Length; i++)
                vmapDatasetErrors[i] = "";

            return new
            {
                Errors = "",
                DatasetProperties = datasetPropertiesArray.ToList(),
                VmapProperties = datasetPropertiesArray.ToList(),
                VmapErrors = vmapErrors,
                VmapDatasetErrors = vmapDatasetErrors,
                Vmap = vmapToSend
            };
        }


        private HashSet<int> GetPropertiesIdsFromDatasetFileArray(Measurement[] datasetFileArray)
        {
            HashSet<int> uniqueProperties = new HashSet<int>();
            foreach (var item in datasetFileArray)
            {
                uniqueProperties.Add(item.TemporalPropertyID);

            }
            return uniqueProperties;
        }
        private object ProcessValidatedMetadataFile(VariableMetadata[] metadataArray, Measurement[] datasetArray, List<string> errors)
        {
            List<int> vmapProperties = new List<int>();
            List<int> datasetProperties = GetPropertiesIdsFromDatasetFileArray(datasetArray).OrderBy(x => x).ToList();
            int datasetPropertiesLength = datasetProperties.Count;
            string[] missingFromMetadataFileErrors = new string[datasetPropertiesLength];
            int vmapIdsLength = datasetPropertiesLength;
            string[] missingFromDatasetFileErrors = new string[vmapIdsLength];
            for (int i = 0; i < missingFromDatasetFileErrors.Length; i++)
                missingFromDatasetFileErrors[i] = "";
            for (int i = 0; i < missingFromMetadataFileErrors.Length; i++)
                missingFromMetadataFileErrors[i] = "";
            //for (int i = 0; i < metadataArray.Length; i++)
            //{
          

            //    var varaiableMetadata = metadataArray[i];
            //    Match temporalPropertyNameMatch = Regex.Match(varaiableMetadata.TemporalPropertyName, "^[a-zA-Z0-9]*$");
            //    if (!temporalPropertyNameMatch.Success)
            //    {
            //        return new
            //        {
            //            Errors = "Please enter only alphanumeric characters in Name & Description",
            //            Vmap = metadataArray,
            //            VmapErrors = missingFromDatasetFileErrors,
            //            VmapDatasetErrors = missingFromMetadataFileErrors,
            //            DatasetProperties = datasetProperties,
            //            VmapProperties = vmapProperties

            //        };
            //    }
            //}
           
            vmapIdsLength = metadataArray.Length;
            missingFromDatasetFileErrors = new string[vmapIdsLength];
            for (int i = 0; i < metadataArray.Length; i++)
                vmapProperties.Add(metadataArray[i].TemporalPropertyID);
            for (int i = 0; i < missingFromDatasetFileErrors.Length; i++)
                missingFromDatasetFileErrors[i] = "";

            for (int i = 0; i < vmapProperties.Count; i++)
            {
                // dataset doesn't contain property that is in vmap
                if (!datasetProperties.Contains(vmapProperties[i]))
                {
                    missingFromDatasetFileErrors[i] = "Variable id " + vmapProperties[i].ToString() + " doesn't exist in dataset";
                    errors.Add(missingFromDatasetFileErrors[i]);
                }
            }


            for (int i = 0; i < datasetProperties.Count; i++)
            {
                // dataset doesn't contain property that is in vmap
                if (!vmapProperties.Contains(datasetProperties.ToArray()[i]))
                {
                    missingFromMetadataFileErrors[i] = "Variable id " + (datasetProperties.ToArray()[i]).ToString() + " is missing from your variable map file";
                    errors.Add(missingFromMetadataFileErrors[i]);
                }
            }
            return new
            {
                Errors = errors,
                Vmap = metadataArray,
                VmapErrors = missingFromDatasetFileErrors,
                VmapDatasetErrors = missingFromMetadataFileErrors,
                DatasetProperties = datasetProperties,
                VmapProperties = vmapProperties

            };
        }
        public object ProcessMetadataFile(HttpPostedFileBase vmapFile, HttpPostedFileBase datasetFile, string pathToSave)
        {
            try
            {
                bool vmapFileValidated = false;
                int lineNumber = 1;
                List<string> errors = new List<string>();

                TextReader textReader = new StreamReader(vmapFile.InputStream);
                GenericParser parser = new GenericParser(textReader)
                {
                    ColumnDelimiter = ','
                };
                // Read header
                parser.Read();

                string TemporalPropertyIDHeader = parser[0];
                string TemporalPropertyNameHeader = parser[1];
                string DescriptionHeader = parser[2];
                List<int> vmapIds = new List<int>();
                List<string> vmapNames = new List<string>();
                List<string> descriptions = new List<string>();
                List<VariableMetadata> variableMetadataList = new List<VariableMetadata>();
                Dictionary<string, List<string>> linesDict = new Dictionary<string, List<string>>();
                Dictionary<string, string> duplicateLinesDict = new Dictionary<string, string>();
            

                if (!String.Equals(TemporalPropertyIDHeader, "TemporalPropertyID"))
                {
                    errors.Add("TemporalPropertyID column header not found");
                    vmapFileValidated = false;
                }
                if (!String.Equals(TemporalPropertyNameHeader, "TemporalPropertyName"))
                {
                    errors.Add("TemporalPropertyName column header not found");
                    vmapFileValidated = false;
                }
                if (!String.Equals(DescriptionHeader, "Description"))
                {
                    errors.Add("Description column header not found");
                    vmapFileValidated = false;
                }

                while (parser.Read())
                {
                    VariableMetadata variableMetadata = new VariableMetadata();
                    if (parser.ColumnCount < 3)
                    {
                        if(parser.ColumnCount == 1)
                        {
                            if(int.TryParse(parser[0], out int parsedId))
                            {
                                variableMetadata.TemporalPropertyID = parsedId;
                            }
                            else
                            {
                                errors.Add("TemporalPropertyID field in line " + lineNumber + " must be an integer");
                            }
                            variableMetadata.TemporalPropertyName = "";
                            variableMetadata.Description = "";
                        }
                        if(parser.ColumnCount == 2)
                        {
                            if (int.TryParse(parser[0], out int parsedId))
                            {
                                variableMetadata.TemporalPropertyID = parsedId;
                            }
                            else
                            {
                                errors.Add("TemporalPropertyID field in line " + lineNumber + " must be an integer");
                            }
                            variableMetadata.TemporalPropertyName = parser[1];
                            variableMetadata.Description = "";


                        }
                        errors.Add("Missing fields in line " + lineNumber);
                        vmapFileValidated = false;
                    }



                    if (parser.ColumnCount > 3)
                    {
                        errors.Add("Too many fields in line " + lineNumber);
                        vmapFileValidated = false;
                        if (int.TryParse(parser[0], out int parsedId))
                        {
                            variableMetadata.TemporalPropertyID = parsedId;
                        }
                        else
                        {
                            errors.Add("TemporalPropertyID field in line " + lineNumber + " must be an integer");
                        }
                        variableMetadata.TemporalPropertyName = parser[1];
                        variableMetadata.Description = parser[2];
                    }

                    if (parser.ColumnCount == 3)
                    {
                        if (int.TryParse(parser[0], out int parsedId))
                        {
                            variableMetadata.TemporalPropertyID = parsedId;
                        }
                        else
                        {
                            errors.Add("TemporalPropertyID field in line " + lineNumber + " must be an integer");
                            vmapFileValidated = false;

                        }
                        variableMetadata.TemporalPropertyName = parser[1];
                        variableMetadata.Description = parser[2];
                    }

                    lineNumber += 1;
                    variableMetadataList.Add(variableMetadata);
                }


                VariableMetadata[] metadataArray = variableMetadataList.ToArray();
                /*metadataFileHandler.ReadHttpPostedFileBaseToArray(vmapFile)*/

                Measurement[] datasetArray = datasetFileHandler.ReadHttpPostedFileBaseToArray(datasetFile);
                return ProcessValidatedMetadataFile(metadataArray, datasetArray, errors);
            }
            catch(Exception ex)
            {
                return new
                {
                    Errors = ex.Message,
                    Vmap = new List<VariableMetadata>() { new VariableMetadata(){
                Description ="a", TemporalPropertyID =1, TemporalPropertyName ="agas"} }
                };
            }


            return new { };
        }

        public Dataset GetDataset(HttpPostedFileBase datasetFile)
        {
            //string datasetPath = fileTransferrer.GetDatasetPath(datasetFile);
            //Dataset dataset = datasetRepository.GetByPath(datasetPath);
            //if (dataset != null && dataset.Visibility == "Public")
            //    return dataset;
            return null;
        }
    }
}
   