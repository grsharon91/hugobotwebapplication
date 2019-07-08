using FileHelpers;
using GenericParsing;
using HugoBotWebApplication.Models.Formats_Handling;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Utils.FileHandlers
{
    public class InputValidationObject
    {
        private bool _isValid;
        private List<string> _errors;

        public InputValidationObject(bool isValid, List<string> errors)
        {
            _isValid = isValid;
            _errors = errors;
        }

        public bool IsValid { get => _isValid;  }
        public List<string> Errors { get => _errors; }
    }
    public class InputHandler
    {
        private string _path;
        private string _vmapPath;
        private readonly HttpFileCollectionBase _files;
		public bool vmapExists { get; set; }
        public byte[] fileArr { get; set; }


		public HttpFileCollectionBase Files => _files;

        public string DatasetPath { get => _path; }
        public string VmapPath { get => _vmapPath; }
		public VariableMetadata[]  ReadMetadataToArray()
		{
			var engine = new FileHelperEngine<VariableMetadata>();
			var vmap = engine.ReadFile(_vmapPath);
			return vmap;
		}
		public InputHandler(HttpFileCollectionBase files, string inputFolder )
        {
            _files = files;
            var datasetFile = _files["datasetFile"];
            HttpPostedFileBase vmapFile;
            HttpPostedFileBase expertFile;
            DateTime date = DateTime.Now;

            try
            {
                expertFile = _files["expert_param"];
                
            }
            catch
            {

            }
            try
            {
                vmapFile = _files["vmapFile"];
                _vmapPath = Path.Combine(inputFolder, datasetFile.FileName.Substring(0, datasetFile.FileName.Length - 4) + "_Vmap.csv");
                vmapFile.SaveAs(_vmapPath);
				vmapExists = true;
            }
            catch
            {
				vmapExists = false;	
			}
            Path.Combine(datasetFile.FileName);
            _path = Path.Combine(inputFolder, datasetFile.FileName);//, datasetFile.FileName.Substring(0, datasetFile.FileName.Length - 4) + "_" +
                        // date.ToString("yyyy_MM_dd_H_mm_ss") + "csv");
            datasetFile.SaveAs(_path);

            _files = files;
        }

        public byte [] getFileToArray()
        {
            var file = _files["datasetFile"];
            //  FileStream stream = new FileStream(_path, FileMode.Create);
            //byte[] ans = new byte[file.InputStream.Length];
            fileArr = new byte[file.InputStream.Length];
            file.InputStream.Read(fileArr, 0, (int) file.InputStream.Length);
           // stream.Read(ans, 0, (int)stream.Length);
            return fileArr;
        }

        
        public InputValidationObject ValidateDatasetFiles()
        {
            bool datasetFileValidated = false;
            int lineNumber = 1;
            List<string> errors = new List<string>();
            byte[] fileBytes = File.ReadAllBytes(_path);
            Stream memoryStream = new MemoryStream();

            TextReader textReader = new StreamReader(memoryStream);
            memoryStream.Write(fileBytes, 0, fileBytes.Length);
            textReader.Read();
            memoryStream.Flush();
            memoryStream.Position = 0;
            GenericParser parser = new GenericParser(textReader)
            {
                ColumnDelimiter = ','
            };
            // Read header
            parser.Read();

            string entityIDHeader = parser[0];
            string TemporalPropertyIDHeader = parser[1];
            string TimeStampHeader = parser[2];
            string TemporalPropertyValueHeader = parser[3];
            Dictionary<string, List<string>> linesDict = new Dictionary<string, List<string>>();
            Dictionary<string, string> duplicateLinesDict = new Dictionary<string, string>();
            if (!String.Equals(entityIDHeader, "EntityID"))
            {
                errors.Add("EntityID column header not found");
                datasetFileValidated = false;
            }

            if (!String.Equals(TemporalPropertyIDHeader, "TemporalPropertyID"))
            {
                errors.Add("TemporalPropertyID column header not found");
                datasetFileValidated = false;
            }
            if (!String.Equals(TimeStampHeader, "TimeStamp"))
            {
                errors.Add("TimeStamp column header not found");
                datasetFileValidated = false;
            }
            if (!String.Equals(TemporalPropertyValueHeader, "TemporalPropertyValue"))
            {
                errors.Add("TemporalPropertyValue column header not found");
                datasetFileValidated = false;
            }
            
            while (parser.Read())
            {
                if(parser.ColumnCount < 4)
                {
                    errors.Add( "Missing fields in line " + lineNumber);
                    datasetFileValidated = false;
                }
                    


                if (parser.ColumnCount > 4)
                {
                    errors.Add( "Too many fields in line " + lineNumber);
                    datasetFileValidated = false;
                }
                
                if(parser.ColumnCount == 4)
                {
                    
                    string entityIDValue = parser[0];
                    string TemporalPropertyIDValue = parser[1];
                    string TimeStampValue = parser[2];
                    string TemporalPropertyValueValue = parser[3];
                    string row = entityIDValue + "," + TemporalPropertyIDValue + "," + TimeStampValue + "," + TemporalPropertyValueValue;
                    if (linesDict.ContainsKey(row))
                    {
                        linesDict[row].Add(row + "_" + lineNumber);
                        string duplicateLinesError = "lines ";
                        foreach (var item in linesDict[row])    
                        {
                            duplicateLinesError += item.Split('_')[1] + ", ";
                        }
                        duplicateLinesError += " are duplicate lines";
                        duplicateLinesDict[row] = duplicateLinesError;
                   
                        datasetFileValidated = false;
                    }
                    else
                    {
                        linesDict.Add(row, new List<string> { row + "_" + lineNumber });
                    }

                    if (!Int32.TryParse(entityIDValue, out int intVal))
                    {
                        errors.Add("EntityID field in line " + lineNumber + " must be an integer");
                        datasetFileValidated = false;
                    }

                    if (!Int32.TryParse(TemporalPropertyIDValue, out intVal))
                    {
                        errors.Add("TemporalPropertyID field in line " + lineNumber + " must be an integer");
                        datasetFileValidated = false;
                    }

                    if (!Int32.TryParse(TimeStampValue, out intVal))
                    {
                        errors.Add("TimeStamp field in line " + lineNumber + " must be an integer");
                        datasetFileValidated = false;
                    }

                    if (!Double.TryParse(TemporalPropertyValueValue, out double doubleVal))
                    {
                        errors.Add("TemporalPropertyValue field in line " + lineNumber + " must be a float");
                        datasetFileValidated = false;

                    }

                }
                lineNumber += 1;
              

            }
            foreach (var item in duplicateLinesDict.Keys)
            {
                errors.Add(duplicateLinesDict[item]);
            }
            return new InputValidationObject(datasetFileValidated, errors);



        }

        public HashSet<int> GetPropertiesIds()
        {
            HashSet<int> uniqueProperties = new HashSet<int>();
            var engine = new FileHelperEngine<Measurement>();

            var result = engine.ReadFile(_path);
            foreach (var item in result)
            {
                uniqueProperties.Add(item.TemporalPropertyID);
               
            }
            return uniqueProperties;
        }

        public object GetProcessedExistingMetadataFile()
        {
            List<int> vmapProperties = new List<int>();
            List<int> datasetProperties = GetPropertiesIds().OrderBy(x => x).ToList();
            int datasetPropertiesLength = datasetProperties.Count;
            string[] missingFromMetadataFileErrors = new string[datasetPropertiesLength];
            int vmapIdsLength = datasetPropertiesLength;
            string[] missingFromDatasetFileErrors = new string[vmapIdsLength];


            for (int i = 0; i < missingFromDatasetFileErrors.Length; i++)
                missingFromDatasetFileErrors[i] = "";
            for (int i = 0; i < missingFromMetadataFileErrors.Length; i++)
                missingFromMetadataFileErrors[i] = "";

            VariableMetadata [] vmap = ReadMetadataToArray();
            vmapIdsLength = vmap.Length;
            missingFromDatasetFileErrors = new string[vmapIdsLength];
            for (int i = 0; i < vmap.Length; i++)
                vmapProperties.Add(vmap[i].TemporalPropertyID);
            for (int i = 0; i < missingFromDatasetFileErrors.Length; i++)
                missingFromDatasetFileErrors[i] = "";

            for (int i = 0; i < vmapProperties.Count; i++)
            {
                // dataset doesn't contain property that is in vmap
                if (!datasetProperties.Contains(vmapProperties[i]))
                    missingFromDatasetFileErrors[i] = "Variable id " + vmapProperties[i].ToString() + " doesn't exist in dataset";
            }


            for (int i = 0; i < datasetProperties.Count; i++)
            {
                // dataset doesn't contain property that is in vmap
                if (!vmapProperties.Contains(datasetProperties.ToArray()[i]))
                {
                    missingFromMetadataFileErrors[i] = "Variable id " + (datasetProperties.ToArray()[i]).ToString() + " is missing from your metadata file";
                }
            }
            return  new
            {
                Errors = "",
                Vmap = vmap,
                VmapErrors = missingFromDatasetFileErrors,
                VmapDatasetErrors = missingFromMetadataFileErrors,
                DatasetProperties = datasetProperties,
                VmapProperties = vmapProperties

            };
        }

        public object GetNewMetadataFile()
        {
            List<int> vmapProperties = new List<int>();
            List<int> datasetProperties = GetPropertiesIds().OrderBy(x => x).ToList();
            int datasetPropertiesLength = datasetProperties.Count;
            string[] missingFromMetadataFileErrors = new string[datasetPropertiesLength];
            int vmapIdsLength = datasetPropertiesLength;
            string[] missingFromDatasetFileErrors = new string[vmapIdsLength];


            for (int i = 0; i < missingFromDatasetFileErrors.Length; i++)
                missingFromDatasetFileErrors[i] = "";
            for (int i = 0; i < missingFromMetadataFileErrors.Length; i++)
                missingFromMetadataFileErrors[i] = "";

            List<VariableMetadata> metadataFile = new List<VariableMetadata>();
            var datasetPropertiesArray = datasetProperties.ToArray();
            for (int i = 0; i < datasetPropertiesArray.Length; i++)
            {
                metadataFile.Add(new VariableMetadata()
                {
                    TemporalPropertyID = datasetPropertiesArray[i],
                    TemporalPropertyName = "",
                    Description = "",
                });
            }
            return new
            {
                Errors = "",
                DatasetProperties = datasetProperties,
                VmapProperties = datasetProperties,
                VmapErrors = missingFromDatasetFileErrors,
                VmapDatasetErrors = missingFromMetadataFileErrors,
                Vmap = metadataFile
            };
        }
    }
}