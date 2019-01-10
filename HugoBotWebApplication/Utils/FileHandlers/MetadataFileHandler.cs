using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;
using FileHelpers;
using HugoBotWebApplication.Models.Formats_Handling;

namespace HugoBotWebApplication.Utils.FileHandlers
{
    public class MetadataFileHandler: IFileHandler<VariableMetadata>
    {
        public byte[] GetBytesFromArray(VariableMetadata[] fileArray)
        {
            FileHelperEngine <VariableMetadata> engine = new FileHelperEngine<VariableMetadata>();
            engine.HeaderText = engine.GetFileHeader();
            MemoryStream fileTarget = new MemoryStream();
            TextWriter textWriter = new StreamWriter(fileTarget);
            engine.WriteStream(textWriter, fileArray);
            textWriter.Flush();
            byte[] metadataFileBytes = fileTarget.ToArray();
            return metadataFileBytes; 
        }

        public byte[] GetBytesFromFile(string path)
        {
            throw new NotImplementedException();
        }

        public VariableMetadata[] ReadFileToArray(string vmapPath)
        {
            VariableMetadata[] metadata = { };
            try
            {
                var vmapFile = new Discretistation.FileHandler().GetFile(vmapPath);
                System.IO.File.WriteAllBytes("C:\\Users\\fayndani\\Foo.txt", vmapFile);
                var vmapEngine = new FileHelperEngine<VariableMetadata>();
                metadata = vmapEngine.ReadFile("C:\\Users\\fayndani\\Foo.txt");
                System.IO.File.Delete("C:\\Users\\fayndani\\Foo.txt");
            }
            catch (Exception)
            {

            }
            return metadata;
        }

        public void WriteFile(string vmapPath)
        {
            throw new NotImplementedException();
        }
        public object ValidateFileBase(HttpPostedFileBase vmapFile)
        {
            object[] validationObject = new object[2];
           
            try
            {
                //var metadataArray = engine.ReadStream(textReader);
                var metadataArray = 1;
                validationObject[0] = "";
                validationObject[1] = metadataArray;
                var jsonObject = new
                {
                    Errors = "",
                    MetadataArray = metadataArray
                };
                return jsonObject;
            }
            catch(Exception ex)
            {
                var jsonObject = new
                {
                    Errors = ex.Message,
                };
                return jsonObject;
            }
           

        }

        public VariableMetadata[] ReadHttpPostedFileBaseToArray(HttpPostedFileBase vmapFile)
        {
            FileHelperEngine<VariableMetadata> engine = new FileHelperEngine<VariableMetadata>();
            TextReader textReader = new StreamReader(vmapFile.InputStream);
            engine.HeaderText = engine.GetFileHeader();
            VariableMetadata[] metadataArray = engine.ReadStream(textReader);
           
            return metadataArray;
        }
    }
}