using System;
using System.Linq;
using System.Threading.Tasks;
using System.Web.Mvc;
using HugoBotWebApplication.Models;
using System.IO;
using Microsoft.AspNet.Identity;
using FileHelpers;
using HugoBotWebApplication.Models.Formats_Handling;
using HugoBotWebApplication.ViewModels;
using HugoBotWebApplication.Services;
using System.Collections.Generic;
using HugoBotWebApplication.Models.Repositories;
using HugoBotWebApplication.Utils.FileHandlers;
using HugoBotWebApplication.CommunicationLayer;
using System.Data.Entity.Validation;
using System.Net;
using System.Data.Entity;
using System.IO.Compression;
using static HugoBotWebApplication.Utils.Settings;
namespace HugoBotWebApplication.Controllers
{
    public class DiscretizationsController : Controller
    {
        private readonly  ApplicationDbContext db;
        private readonly DatasetRepository datasetRepository;
        private readonly DiscretizationRepository discretizationRepository;
        private readonly DistanceMeasureDiscretizationRepository distanceMeasuerDiscretizationRepository;
        private readonly DatasetService datasetService;
        private DiscretizationService discretizationService = new DiscretizationService();
        private readonly SecurityService securityService;
        private int id;
        public DiscretizationsController()
        {
            db = new ApplicationDbContext();
            datasetRepository = new DatasetRepository(db);
            discretizationRepository = new DiscretizationRepository(db);
            distanceMeasuerDiscretizationRepository = new DistanceMeasureDiscretizationRepository(db);
            securityService = new SecurityService(datasetRepository, db);
            datasetService = new DatasetService(datasetRepository);
            id = discretizationRepository.GetNextId();
        }
        // GET: Discretizations/Create
        public ActionResult Create()
        {
            return View();
        }
		public ActionResult GetDiscretizations(int id)
		{
            Discretization disc = discretizationRepository.Get(id);
            string path = discretizationService.getPath(datasetService.getPath(disc.DatasetID), id);
            string fullPath = Server.MapPath(path);
            string tmp = fullPath + "\\tmp";
            Directory.CreateDirectory(tmp);
            string archive = fullPath + "\\Discretizations.zip";
            foreach (string file in Directory.GetFiles(fullPath))
            {
                System.IO.File.Copy(file, Path.Combine(tmp, Path.GetFileName(file)));
            }
            ZipFile.CreateFromDirectory(tmp, archive);
            Directory.Delete(tmp,true);
            FileStream files = new FileStream(archive, FileMode.Open, FileAccess.Read);
            int len = (int)(files.Length);
            Byte[] content = new Byte[len];
            files.Read(content, 0, len);
            files.Close();
            System.IO.File.Delete(archive);
            return File(content, ".zip", "Discretizations" + DateTime.Now.ToShortDateString() + ".zip");
        }

		public string DownloadDiscretizations(int [] discretizationIdList)
		{
            List<Discretization> discretizations = discretizationIdList.Select(id => discretizationRepository.Get(id)).ToList();
            string downloadPath = discretizationService.GetDownloadPath(discretizations);
            return downloadPath;
		}

        public string DownloadDiscretization(int ID)
        {
            string downloadPath = discretizationRepository.Get(ID).DownloadPath;
            return downloadPath;
        }

        public async Task<ActionResult> Edit(int? id)
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
            FileTransferrer fileTransferrer = new FileTransferrer();
            foreach (var disc in dataset.Discretizations)
            {

                string discPath = discretizationService.getPath(datasetService.getPath(dataset.DatasetID), disc.DiscretizationID);
                discPath += "/KL.txt";
                if (System.IO.File.Exists(Server.MapPath(discPath)))
                {
                    disc.ParametersIsReady = "Ready";
                }
                else
                {
                    disc.ParametersIsReady = "In Progress";
                }
                discretizationRepository.Edit(disc);
            }
            datasetRepository.SaveChanges();
            return View(new DiscretizationExistingViewModel()
            {
                DatasetID = (int)id,
                Discretizations = dataset.Discretizations,
                Dataset = dataset
          

            });
        }

        public string SendToDiscretization(SendDiscretizationViewModel sendDiscretizationViewModel)
		{
			string[] methodsList = Request.Form["Methods"].Split(',');
			var  knowledgeBasedMethods = Request.Form["KnowledgedBasedMethods"].Split(',');
			FileTransferrer fileTransferrer = new FileTransferrer();
			Dataset dataset = db.Datasets.Find(sendDiscretizationViewModel.id);
			string currentUserId = User.Identity.GetUserId();
			ApplicationUser currentUser = db.Users.FirstOrDefault(y => y.Id == currentUserId);
           
            // Check that there are *not* knowledge based methods in the request
            if(methodsList[0] != "")
            {
                discretizationService.Discretize(methodsList, datasetService.getPath(dataset.DatasetID), id);
                List<Discretization> discretizations = discretizationService.CreateDiscretizations(dataset, methodsList, id, datasetService.getPath(dataset.DatasetID));
                for (int i = 0; i < discretizations.Count; i++)
                {
                    discretizations[i].Owner = currentUser;
                    discretizationRepository.Add(discretizations[i]);
                }
            }

            // Knowledge based methods with files uploaded

            if (Request.Files.Count > 0)
			{
				foreach (var knowledgeBasedMethod in knowledgeBasedMethods)
				{
					var knowledgeBasedMethodSplit = knowledgeBasedMethod.ToString().Split('_');
					var methodName = knowledgeBasedMethodSplit[0];
					var fileName = knowledgeBasedMethodSplit[knowledgeBasedMethodSplit.Length - 1];
					var maxGap = knowledgeBasedMethodSplit[1];
					var windowSize = knowledgeBasedMethodSplit[2];
					var statesFilyBytes = fileTransferrer.GetBytesFromFile(Request.Files[fileName]);
					var methodDownloadPath = fileTransferrer.ExpertDataset(dataset.Path, methodName+ "/" + maxGap + "_" + windowSize, statesFilyBytes);

                    Discretization d = new Discretization()
					{
						Dataset = dataset,
						DownloadPath = methodDownloadPath,
						Visibility = "",
						Type = "Discretized",
						Owner = currentUser,
						FullName = MethodEncodingToMethodName[methodName],
						ParametersIsReady = "In Progress"
					};
					db.Discretizations.Add(d);
				}
			
			}
			discretizationRepository.SaveChanges();
			return "Discretizing...";
			
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
