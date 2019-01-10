using FileHelpers;
using HugoBotWebApplication.Models.Formats_Handling;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Utils.FileHandlers
{
    public class DatasetFileHandler : IFileHandler<Measurement>
    {
        public byte[] GetBytesFromArray(Measurement[] fileArray)
        {
            throw new NotImplementedException();
        }

        public byte[] GetBytesFromFile(string path)
        {
            throw new NotImplementedException();
        }

        public Measurement[] ReadFileToArray(string path)
        {
            throw new NotImplementedException();
        }

        public Measurement[] ReadHttpPostedFileBaseToArray(HttpPostedFileBase datasetFile)
        {
            FileHelperEngine<Measurement> engine = new FileHelperEngine<Measurement>();
            TextReader textReader = new StreamReader(datasetFile.InputStream);
            engine.HeaderText = engine.GetFileHeader();
            Measurement[] metadataArray = engine.ReadStream(textReader);

            return metadataArray;
        }

        public object ValidateFileBase(HttpPostedFileBase fileBase)
        {
            throw new NotImplementedException();
        }

        public void WriteFile(string path)
        {
            throw new NotImplementedException();
        }
    }
}