using HugoBotWebApplication.Models;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.CommunicationLayer
{
    public class FileTransferrer
    {
        private Discretistation.FileHandler discretistationFileHandler = new Discretistation.FileHandler();

        public FileTransferrer()
        {

        }

		public byte[] GetFilesFromServer(string path)
		{
			return discretistationFileHandler.GetFile(path);
		}

        public byte[] GetBytesFromFile(HttpPostedFileBase file)
        {
            byte[] fileBytes = new byte[file.ContentLength];
            file.InputStream.Read(fileBytes, 0, file.ContentLength);
            file.InputStream.Flush();
            return fileBytes;
        }


        public string SendDatasetFiles(string datasetName, byte[] datasetFileBytes,byte[] vmapFileBytes)
        {
            return discretistationFileHandler.SendDatasetAndVmapToServer(datasetName,
              datasetFileBytes,
              vmapFileBytes);
        }
        public string SendEntitiesFile(string datasetPath, byte[] entitiesFileBytes)
        {
            discretistationFileHandler.UploadEntities(datasetPath, entitiesFileBytes);
            return "Success";
        }
        public string SendDatasetFiles(string datasetName, HttpPostedFileBase datasetFile, HttpPostedFileBase vmapFile)
        {
            
            return discretistationFileHandler.SendDatasetAndVmapToServer(datasetName, 
                GetBytesFromFile(datasetFile), 
                GetBytesFromFile(vmapFile));

        }
        public string GetDatasetPath(HttpPostedFileBase datasetFile)
        {
            string hex = "";
            return discretistationFileHandler.IsDatasetExists(GetBytesFromFile(datasetFile), out hex);
        }
        public string DescretizeDataset(string paramsToSend)
        {
            return discretistationFileHandler.Discretization(paramsToSend);
        }
        public string DiscretizeDataset(string datasetPath, string paramsToSend)
        {
            return discretistationFileHandler.Discretization(datasetPath + "/" + paramsToSend); 
        }
        public string ExpertDataset(string datasetPath, string paramsToSend, byte [] cutpoints)
        {
            return discretistationFileHandler.ExpertDiscretization(datasetPath + "/" +paramsToSend, cutpoints);
        }

        public string SendDatasetFileToDiscretization()
        {
            return "";
        }
        //public string SendFiles()
    }
}