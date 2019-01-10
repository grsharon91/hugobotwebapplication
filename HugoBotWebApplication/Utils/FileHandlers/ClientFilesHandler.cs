//using System;
//using System.Collections.Generic;
//using System.IO;
//using System.Linq;
//using System.Web;

//namespace HugoBotWebApplication.Utils.FileHandlers
//{
//    protected class ClientFilesHandler
//    {
//        private HttpFileCollectionBase _files;
//        private string[] _fileNames = { "Path", "Vmap_file" };
//        private bool FilesExist(HttpFileCollectionBase files)
//        {
            

//            return true;
//        }
//        public ClientFilesHandler(HttpFileCollectionBase files)
//        {
//            var datasetFile = _files["Path"];
//            var vmapFile = _files["Vmap_file"];
//            var path = Path.Combine(Server.MapPath("~/App_Data/uploads"), datasetFile.FileName);
//            datasetFile.SaveAs(path);
//            var vmap_path = Path.Combine(Server.MapPath("~/App_Data/uploads"), datasetFile.FileName + "_Vmap");
//            vmapFile.SaveAs(vmap_path);
//            _files = files;
//        }

//        public HttpFileCollectionBase Files { get => _files;}
//    }
//}