﻿using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Threading.Tasks;
using System.Net;
using System.Web.Mvc;
using HugoBotWebApplication.Models;
using FileHelpers;
using HugoBotWebApplication.Models.Formats_Handling;
using HugoBotWebApplication.ViewModels;
using Microsoft.AspNet.Identity;
using HugoBotWebApplication.Models.Repositories;
using HugoBotWebApplication.Utils.FileHandlers;
using HugoBotWebApplication.CommunicationLayer;
using HugoBotWebApplication.Services;
using System.Data.Entity.Validation;
using System.IO;
using System.Web;

namespace HugoBotWebApplication.Controllers
{
    public class DatasetsController : Controller
    {
        private ApplicationDbContext db;
        private static DatasetRepository datasetRepository;
        private static  DiscretizationRepository discretizationRepository;
        private readonly DatasetService datasetService;
        private readonly DiscretizationService discretizationService = new DiscretizationService();
        private readonly SecurityService securityService;
        private byte[] fileArr;
        private MetadataViewModel metadataViewModel = new MetadataViewModel();
        public DatasetsController ()
        {
            db = new ApplicationDbContext();
            datasetRepository = new DatasetRepository(db);
            discretizationRepository = new DiscretizationRepository(db);
            datasetService = new DatasetService(datasetRepository);
            securityService = new SecurityService(datasetRepository);

        }
        // GET: Datasets
        // TODO
        public ActionResult Index()
        {
            var discretistationFileHandler = new Discretistation.FileHandler();
            var datasetList = datasetRepository.GetAll();
            foreach (var dataset in datasetList)
            {
                foreach (var disc in dataset.Discretizations)
                {
                   // disc.ParametersIsReady = discretistationFileHandler.IsFileExists(disc.DownloadPath);
                        //disc.ParametersIsReady = "Ready";
                    discretizationRepository.Edit(disc);

                }
            }

            discretizationRepository.SaveChanges();
            var testStuff = datasetRepository.GetAll().Where(item => item.Owner.Email == User.Identity.Name).ToList();
            DatasetIndexViewModel datasetIndexViewModel = new DatasetIndexViewModel()
            {
                Datasets = datasetRepository.GetAll()
            };
            return View(datasetIndexViewModel);
        }
		public ActionResult OwnedDatasets()
		{
			string currentUserId = User.Identity.GetUserId();
			DatasetIndexViewModel datasetIndexViewModel = new DatasetIndexViewModel()
			{
				//DatasetsRecords = new List<string>(),
				Datasets = datasetRepository.GetAll().Where(d => d.Owner != null && d.Owner.Id == currentUserId).ToList()
			};
			return View(datasetIndexViewModel);
		}

        // GET: Datasets/Details/5
        public ActionResult Details(int? id)
        {
            if (id == null)
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            string currentUserId = User.Identity.GetUserId();
           
            Dataset dataset = datasetRepository.Get((int)id);

            if (dataset == null)
                return HttpNotFound();

            if (dataset.Visibility == "Private" && !securityService.HasAccess((int)id, currentUserId))
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);

            DatasetDetailsViewModel datasetDetailsViewModel = datasetService.CreateDatasetDetailsViewModel(dataset);
            dataset.NumberOfViews += 1;
            datasetRepository.Edit(dataset);
            datasetRepository.SaveChanges();
            return View(datasetDetailsViewModel);
        }

        public ActionResult DownloadExampleOriginalDataset()
        {
            string examplePath = Server.MapPath(("~/App_Data/test_files/toy.csv"));
            byte[] exampleOriginalDataset = System.IO.File.ReadAllBytes(examplePath);
            return File(exampleOriginalDataset, "text/csv", "Hugo_example_orginal_dataset" + ".csv");
        }
        public ActionResult DownloadExampleHugoDataset()
        {
            string examplePath = Server.MapPath(("~/App_Data/test_files/ToyHugo.csv"));
            byte[] exampleOriginalDataset = System.IO.File.ReadAllBytes(examplePath);
            return File(exampleOriginalDataset, "text/csv", "Hugo_example_formatted_dataset" + ".csv");
        }
        public ActionResult DownloadExampleVariableMap()
        {
            string examplePath = Server.MapPath(("~/App_Data/test_files/toy_vmap.csv"));
            byte[] exampleOriginalDataset = System.IO.File.ReadAllBytes(examplePath);
            return File(exampleOriginalDataset, "text/csv", "Hugo_example_variable_map" + ".csv");
        }
        public ActionResult DownloadExampleEntitiesFile()
        {
            string examplePath = Server.MapPath(("~/App_Data/test_files/entities.csv"));
            byte[] exampleOriginalDataset = System.IO.File.ReadAllBytes(examplePath);
            return File(exampleOriginalDataset, "text/csv", "Hugo_example_entities_file" + ".csv");
        }
        public ActionResult DownloadlEntitiesFile(int? id)
        {
            string currentUserId = User.Identity.GetUserId();
            if (currentUserId == null)
                return RedirectToAction("Register", "Account");
            ApplicationUser user = db.Users.Find(currentUserId);
            if (currentUserId != null && !user.EmailConfirmed)
            {
                return RedirectToAction("Index", "Home");
            }
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }

            Dataset dataset = datasetRepository.Get((int)id);
            if (dataset == null)
            {
                return HttpNotFound();
            }

            if (!securityService.HasAccess((int)id, currentUserId))
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }

            byte[] entitiesFile = datasetService.GetEntitiesFile(dataset);
            return File(entitiesFile, "text/csv", "Dataset_Entities" + DateTime.Now + ".csv");

        }
        public ActionResult DownloadAllDatasetFiles(int? id)
        {
            string currentUserId = User.Identity.GetUserId();
            if (currentUserId == null)
                return RedirectToAction("Register", "Account");
            ApplicationUser user = db.Users.Find(currentUserId);
            if (currentUserId != null && !user.EmailConfirmed)
            {
                return RedirectToAction("Index", "Home");
            }
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            Dataset dataset = datasetRepository.Get((int)id);
            if (dataset == null)
            {
                return HttpNotFound();
            }

            if (!securityService.HasAccess((int)id, currentUserId))
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }


            string inputFolder = Server.MapPath(dataset.Path);

           // string path = Path.Combine(inputFolder, datasetFile.FileName.Substring(0, datasetFile.FileName.Length - 4) + "_Vmap.csv");
            //string path = dataset.Path.Substring(0, dataset.Path.Length - 11);
            //byte[] datasetFiles = dataset.DatasetFile;
            byte[] datasetFile = System.IO.File.ReadAllBytes(inputFolder);
            dataset.NumberOfDownloads += 1;
            datasetRepository.Edit(dataset);
            datasetRepository.SaveChanges();
       
            return File(datasetFile, "text/csv", "Dataset" + DateTime.Now + ".csv");
        }
        public ActionResult DownloadDatasetFile(int? id)
		{
            string currentUserId = User.Identity.GetUserId();
            if (currentUserId == null)
                return RedirectToAction("Register", "Account");
            ApplicationUser user = db.Users.Find(currentUserId);
            if (currentUserId != null && !user.EmailConfirmed)
            {
                return RedirectToAction("Index", "Home");
            }
            if (id == null)
			{
				return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
			}
			Dataset dataset =  datasetRepository.Get((int)id);
			if (dataset == null)
			{
				return HttpNotFound();
			}
            if (!securityService.HasAccess((int)id, currentUserId))
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }

            byte[] datasetFile = datasetService.GetDatasetFile(dataset);

            dataset.NumberOfDownloads += 1;
            datasetRepository.Edit(dataset);
            datasetRepository.SaveChanges();
            return File(datasetFile, "text/csv", "Dataset" + DateTime.Now + ".csv");
		}
		public ActionResult DownloadMetadataFile(int? id)
		{
            string currentUserId = User.Identity.GetUserId();
            if (currentUserId == null)
                return RedirectToAction("Register", "Account");
            ApplicationUser user = db.Users.Find(currentUserId);
            if (currentUserId != null && !user.EmailConfirmed)
            {
                return RedirectToAction("Index", "Home");
            }
            if (id == null)
				return new HttpStatusCodeResult(HttpStatusCode.BadRequest);

            Dataset dataset = datasetRepository.Get((int) id);
			if (dataset == null)
				return HttpNotFound();


            if (!securityService.HasAccess((int)id, currentUserId))
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);

            byte[] metadataFile = datasetService.GetMetadataFile(dataset);
			return File(metadataFile, "text/csv", "Dataset_Vmap" + DateTime.Now + ".csv");
		}
		// GET: Datasets/Create
		public ActionResult Create()
        {
           string currentUserId = User.Identity.GetUserId();
            if (currentUserId == null)
                return RedirectToAction("Register", "Account");
            ApplicationUser user = db.Users.Find(currentUserId);
            if (currentUserId != null && !user.EmailConfirmed)
            {
                return RedirectToAction("Index", "Home");
            }
              
            return View();
        }
		// POST: Datasets/Create
		public string ProcessDatasetFile()
		{
            Dataset dataset = datasetService.GetDataset(Request.Files["datasetFile"]);
            if (dataset != null)
                return "This dataset already exists under the name: " + dataset.DatasetName;
            var datasetFile = Request.Files["datasetFile"];
            DateTime date = DateTime.Now;
            string dir = "~/App_Data/uploads/" + datasetFile.FileName.Substring(0, datasetFile.FileName.Length - 4) + "_" +
                        date.ToString("yyyy_MM_dd_H") + "/";
            string inputFolderPath = Server.MapPath(dir);
            Directory.CreateDirectory(Server.MapPath(dir));
          InputHandler inputHandler = new InputHandler(Request.Files, inputFolderPath);
			InputValidationObject inputValidationObject = inputHandler.ValidateDatasetFiles();
			if (!inputValidationObject.IsValid)
			{
				ViewBag.Errors = String.Join("<br>", inputValidationObject.Errors);
			}
            string path = dir + datasetFile.FileName;
           // FileStream stream = new FileStream(path, FileMode.Create);
            fileArr = new byte[datasetFile.InputStream.Length];
            fileArr = inputHandler.getFileToArray();
            //stream.Read(fileArr, 0, (int)stream.Length);
            //stream.Close();
           // dataset.DatasetFile = file;
            return String.Join("<br>", inputValidationObject.Errors);
		}
		[HttpPost]
		public ActionResult ProcessVmapFile()
		{
            var vmapFile = Request.Files["vmapFile"];
            var datasetFile = Request.Files["datasetFile"];
            //string inputFolderPath = Server.MapPath(("~/App_Data/uploads"));
            //InputHandler inputHandler = new InputHandler(Request.Files, inputFolderPath);
            //InputValidationObject inputValidationObject = inputHandler.ValidateDatasetFiles();
            if (vmapFile != null)
                return Json(datasetService.ProcessMetadataFile(vmapFile, datasetFile, ""));
            else
            {
                return Json(datasetService.CreateMetadataFileFromDatasetFile(datasetFile));
               
            }

        }

        [HttpPost]
        //[ValidateAntiForgeryToken]
        public ActionResult Create(DatasetViewModel datasetViewModel)
        {

            if (ModelState.IsValid)
            {
                string currentUserId = User.Identity.GetUserId();
                ApplicationUser currentUser = db.Users.FirstOrDefault(y => y.Id == currentUserId);

                // Prepare metadata file
                byte[] metadataFileBytes = datasetService.CreateMetadataFile(datasetViewModel.TemporalPropertyID,
                   datasetViewModel.TemporalPropertyName, datasetViewModel.Description);

                // Transfer files
                //string datasetPath = datasetService.UploadDatasetFiles(datasetViewModel.DatasetName, Request.Files["datasetFile"], metadataFileBytes, Request.Files["Entity_file"]);
                string date = DateTime.Now.ToString("yyyy_MM_dd_H");
                string datasetPath = datasetService.getPath(Request.Files["datasetFile"].FileName, date);

                // Create Dataset model
                Dataset dataset = datasetService.CreateDatasetFromDatasetViewModel(datasetViewModel, datasetRepository.GetNextId(), datasetPath, datasetPath + "/vmap", currentUser, metadataFileBytes);
                dataset.Size = ((double)Request.Files["datasetFile"].ContentLength / 1024) / 1024;
                //dataset.DatasetFile = fileArr;
                Stream s = Request.Files["datasetFile"].InputStream;
                BinaryReader br = new BinaryReader(s);
                byte [] file = br.ReadBytes((Int32)s.Length);
                dataset.DatasetFile = file;

                //Save dataset's information in database
                datasetRepository.Add(dataset);
                datasetRepository.SaveChanges();
                //return Json(new { success = true });
                  
                return RedirectToAction("Index");
            }

            return Json(new { success = false });
        }


       
        //TODO
        public ActionResult DownloadFiles(string parameters)
        {
            string currentUserId = User.Identity.GetUserId();
            if (currentUserId == null)
                return RedirectToAction("Register", "Account");
            ApplicationUser user = db.Users.Find(currentUserId);
            if (currentUserId != null && !user.EmailConfirmed)
            {
                return RedirectToAction("Index", "Home");
            }
            var y = 2;

            var parametersList = new HashSet<string>(parameters.Split(' '));
            if (parametersList.Count == 1)
            {
                if (parametersList.ToArray()[0].Split('/').Length == 1)
                {
                    var discretistationFileHandler_1 = new Discretistation.FileHandler();
                    parameters = String.Join(" ", parametersList.ToArray());
                    byte[] downloadedDatasets_1 = discretistationFileHandler_1.GetFile(parameters);
                    //var paramsToSend = String.Join(" " + datasetPath + "/", datasetService.GetParamsToSend().Split(' '));
                    //discretistationFileHandler.GetFile()
                    //var y = 2;
                    string contentType_1 = "text/csv";
                    return File(downloadedDatasets_1, contentType_1, "Datasets" + DateTime.Now + ".csv");
                }

            }

            var discretistationFileHandler = new Discretistation.FileHandler();
            parameters = String.Join(" ", parametersList.ToArray());
            byte[] downloadedDatasets = discretistationFileHandler.GetFile(parameters);
            //var paramsToSend = String.Join(" " + datasetPath + "/", datasetService.GetParamsToSend().Split(' '));
            //discretistationFileHandler.GetFile()
            //var y = 2;
            string contentType = "text/csv";
            return File(downloadedDatasets, contentType, "Datasets" + DateTime.Now + ".zip");


        }
        // TODO
        public string Download(DatasetIndexViewModel datasetIndexViewModel)
        {

            var datasetsRecords = datasetIndexViewModel.DatasetsRecords;
            var discretizationsRecords = datasetIndexViewModel.DiscretizationsRecords;
			var karmaLegoRecords = datasetIndexViewModel.KarmaLegoRecords;
			var discretistationFileHandler = new Discretistation.FileHandler();
            Dictionary<int, string> idToParameters = new Dictionary<int, string>();
            Dictionary<int, bool> idToRawFlag = new Dictionary<int, bool>();
            DatasetService datasetService = new DatasetService(datasetRepository);
            List<string> allParamsToSend = new List<string>();
            if(datasetsRecords != null)
			{
				foreach (var datasetRecord in datasetsRecords)
				{
                    Dataset dataset = datasetRepository.Get(Int32.Parse(datasetRecord));
                    allParamsToSend.Add(dataset.Path);
                    dataset.NumberOfDownloads += 1;
                    datasetRepository.Edit(dataset);
                    datasetRepository.SaveChanges();
                               

                }
			}

            if (discretizationsRecords != null)
            {
                foreach (var discretizationsRecord in discretizationsRecords)
                {
                    var discretization = discretizationRepository.Get(Int32.Parse(discretizationsRecord));
                    var dataset = discretization.Dataset;
                    var datasetPath = dataset.Path;
                    //if()
                    allParamsToSend.Add(discretization.DownloadPath);
                }
            }
            if (karmaLegoRecords != null)
            {
                foreach (var karmaLegoRecord in karmaLegoRecords)
                {
                    var kl = db.KarmaLegos.Find(Int32.Parse(karmaLegoRecord));
                    var discretization = kl.Discretization;
                    var datasetPath = discretization.Dataset.Path;
                    //if()
                    allParamsToSend.Add(kl.DownloadPath);
                }
            }

                var allParamsToSendString = String.Join(" ", allParamsToSend);
                return allParamsToSendString;

       
        }

       
        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                db.Dispose();
            }
            base.Dispose(disposing);
        }
    }
}
