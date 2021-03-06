﻿
using HugoBotWebApplication.Models;
using Microsoft.AspNet.Identity;
using System;
using System.IO;
using System.Linq;
using System.Web.Mvc;
using HugoBotWebApplication.ViewModels;
using HugoBotWebApplication.Services;
using HugoBotWebApplication.Utils.FileHandlers;
using HugoBotWebApplication.CommunicationLayer;
using System.Collections.Generic;
using System.Net;
using HugoBotWebApplication.Models.Repositories;
using System.Data.Entity.Validation;
using System.Data.Entity;
using System.IO.Compression;

namespace HugoBotWebApplication.Controllers
{
    public class KarmaLegoController : Controller
    {
        private ApplicationDbContext db;
        private DiscretizationService discretizationService;
        private KarmaLegoService karmaLegoService;
        private DatasetService datasetService;
        private readonly DatasetRepository datasetRepository;
        private readonly KLRepository klRepository;
        private SecurityService securityService;
        private int id;

        public KarmaLegoController()
        {
            db = new ApplicationDbContext();
            datasetRepository = new DatasetRepository(db);
            klRepository = new KLRepository(db);
            discretizationService = new DiscretizationService();
            karmaLegoService = new KarmaLegoService();
            datasetService = new DatasetService(datasetRepository);
            securityService = new SecurityService(datasetRepository, db);
        }

        public ActionResult GetKarmaLegos(int id)
        {

            string fullPath = db.KarmaLegos.Find(id).DownloadPath;
            //string fullPath = Server.MapPath(path);
            string tmp = fullPath + "\\tmp";
            Directory.CreateDirectory(tmp);
            string archive = fullPath + "\\KarmaLego.zip";
            foreach (string file in Directory.GetFiles(fullPath))
            {
                System.IO.File.Copy(file, Path.Combine(tmp, Path.GetFileName(file)));
            }
            ZipFile.CreateFromDirectory(tmp, archive);
            Directory.Delete(tmp, true);
            FileStream files = new FileStream(archive, FileMode.Open, FileAccess.Read);
            int len = (int)(files.Length);
            Byte[] content = new Byte[len];
            files.Read(content, 0, len);
            files.Close();
            System.IO.File.Delete(archive);
            return File(content, ".zip", "KarmaLego" + DateTime.Now.ToShortDateString() + ".zip");
        }

        public string DownloadKarmaLegos(int[] discretizationIdList)
        {
            FileTransferrer fileTransferrer = new FileTransferrer();
            List<string> downloadPath = new List<string>();
            foreach (var id in discretizationIdList)
            {
                var discretization = db.KarmaLegos.Find(id);
                downloadPath.Add(discretization.DownloadPath);
            }
            return String.Join(" ", downloadPath);
        }

        public string DownloadKarmaLego(int ID)
        {
            var discretization = db.KarmaLegos.Find(ID);
            return discretization.DownloadPath;
        }


        // GET: KarmaLego
        public ActionResult Index(int? id)
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
            Dataset dataset = db.Datasets.Find(id);
            ApplicationUser currentUser = db.Users.FirstOrDefault(y => y.Id == currentUserId);

            if (dataset == null)
            {
                return HttpNotFound();
            }
            if (currentUser.Id != "4b67ae3b-8854-40a2-9751-8021070bf5ba")
            {
                if (dataset == null || (dataset.Owner != null && dataset.OwnerID != currentUserId && dataset.Visibility == "Private" && !securityService.HasAccess(dataset.DatasetID, currentUserId)))
                {
                    return HttpNotFound();
                }
            }
            foreach (var disc in dataset.Discretizations)
            {
                string discPath = discretizationService.getPath(datasetService.getPath(disc.DatasetID), disc.DiscretizationID);
                foreach (var kl in disc.KarmaLegos)
                {
                    string klResultPath = kl.DownloadPath;
                    klResultPath += @"\kl-result.txt";
                    if (System.IO.File.Exists(klResultPath))
                    {
                        kl.IsReady = "Ready";
                    }
                    else
                    {
                        kl.IsReady = "In Progress";
                    }
                    db.Entry(kl).State = EntityState.Modified;

                }

            }
            db.SaveChanges();

            List<Discretization> discretizations = dataset.Discretizations;
            // Discretistation.FileHandler fileHandler = new Discretistation.FileHandler();
            List<KarmaLego> karmaLegos = new List<KarmaLego>();
            Dictionary<int, string[]> klClasses = new Dictionary<int, string[]>();
            foreach (var discretization in discretizations)
            {
                foreach (var kl in discretization.KarmaLegos)
                {
                    karmaLegos.Add(kl);
                }
            }
            foreach (var kl in karmaLegos)
            {  // if(new Discretistation.FileHandler().IsFileExists(kl.DownloadPath)== "Ready" && kl.Fold  == 1)
               //    {
               //        klClasses[kl.KarmaLegoID] = fileHandler.GetClasses(kl.DownloadPath + "/KARMALEGOV");
               //    }
                if (kl.IsReady == "Ready" && kl.Fold == 1)
                {
                    klClasses[kl.KarmaLegoID] = karmaLegoService.getClasses(kl.DownloadPath);
                }
                else
                {
                    klClasses[kl.KarmaLegoID] = new string[] { "" };
                }
            }
            return View(new KarmaLegoIndexViewModel()
            {
                Discretizations = discretizations,
                KarmaLegos = karmaLegos,
                Classes = klClasses,
                Dataset = dataset
            });
        }

        // GET: KarmaLego/Details/5
        public ActionResult Details(int id)
        {
            return View();
        }

        // GET: KarmaLego/Create
        public ActionResult Create()
        {
            return View();
        }
        public string DiscoverPatterns()
        {
            var karmaLegoConfigs = Request.Form["Configs"].Split(',');
            //  List<int> discretizatonsIds = new List<int>();
            //  List<int> currentDiscretizationIds = new List<int>();
            foreach (var klc in karmaLegoConfigs)
            {
                var configs = klc.Split('_');
                var configId = configs[0];
                //  currentDiscretizationIds.Add(Int32.Parse(configId));
            }
            // var configsToSendList = new List<string>();
            if (karmaLegoConfigs[0] != "")
            {
                foreach (var config in karmaLegoConfigs)
                {
                    var configs = config.Split('_');
                    var configId = configs[0];
                    var fold = configs[configs.Length - 1];
                    var configParams = configs.Skip(1).Take(configs.Length - 2).Select(x => x).ToArray();
                    Discretization d = db.Discretizations.Find(Int32.Parse(configId));
                    id = klRepository.GetNextId();
                    var path = discretizationService.getPath(datasetService.getPath(d.DatasetID), d.DiscretizationID);
                    var inputPath = Server.MapPath(path);
                    var karmaLegoPath = inputPath + @"\KARMALEGO\" + id.ToString();
                    inputPath += @"\KL.txt";

                    //if(fold == "1")
                    //{
                    //     karmaLegoPath = d.DownloadPath + "/KARMALEGO/" + String.Join("_", configParams);

                    //}
                    //configsToSendList.Add(karmaLegoPath);
                    string currentUserId = User.Identity.GetUserId();
                    ApplicationUser currentUser = db.Users.FirstOrDefault(y => y.Id == currentUserId);
                    if (!Int32.TryParse(configParams[0], out int tempInt))
                        return "Epslion value is not ok";
                    else
                    {
                        if (tempInt < 0)
                            return "Epslion value is not ok";
                    }
                    if (!Int32.TryParse(configParams[0], out tempInt))
                        return "Maximum gap value is not ok";
                    else
                    {
                        if (tempInt < 0)
                            return "Maximum gap value is not ok";
                    }
                    if (!Double.TryParse(configParams[2], out double tempDouble))
                        return "Vertical support value is not ok";
                    else
                    {
                        if (tempDouble < 0 || tempDouble > 100)
                            return "Vertical support value is not ok";
                    }
                    var epsilon = Double.Parse(configParams[0]);
                    var maxGap = Int32.Parse(configParams[1]);
                    var minVerticalSupport = Double.Parse(configParams[2])/100;
                    karmaLegoService.sendToKL(inputPath, karmaLegoPath, epsilon, minVerticalSupport, maxGap);
                    KarmaLego kl = new KarmaLego()
                    {
                        Discretization = d,
                        Epsilon = epsilon,
                        DownloadPath = karmaLegoPath,
                        IsReady = "In Progress",
                        MaximumGap = maxGap,
                        MinimumVerticalSupport = minVerticalSupport,
                        Owner = currentUser,
                        Fold = Int32.Parse(fold)
                    };
                    //discretizatonsIds.Add(d.DiscretizationID);

                    db.KarmaLegos.Add(kl);
                }
                //var llll = String.Join(" ", configsToSendList);
                db.SaveChanges();
                //List<string> klIds = new List<string>();
                //foreach (var kl in db.KarmaLegos)
                //{
                //    if(discretizatonsIds.IndexOf(kl.DiscretizationID) != -1 )
                //        klIds.Add(kl.KarmaLegoID.ToString());
                //}
                return "Success";
                //return Json(new
                //{
                //    Ids = String.Join("_", klIds),
                //    Classes = "Class1,Class2_Class3,Class4",
                //    Errors = ""
                //});

            }
            return "Error";
            //return Json(new
            //{
            //    Errors = "ERRORS"

            //});
        }
        [HttpPost]
        public string VisualizePatterns()
        {
            var karmaLegoIdChosen = Request.Form["Id"];
            // add merge option
            var klClassChosen = Request.Form["Class"];

            KarmaLego kl = db.KarmaLegos.Find(Int32.Parse(karmaLegoIdChosen));
            Dataset dataset = db.Datasets.Find(kl.Discretization.DatasetID);
            Discretistation.FileHandler fh = new Discretistation.FileHandler();

            Session["correntPathToIndex"] = kl.DownloadPath + "/KARMALEGOV/" + klClassChosen;
            Session["dataset"] = dataset;
            Session["discConfig"] = kl.Discretization.DownloadPath;


            return "";
        }

        public ActionResult Edit(int? id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            Discretization discretization = db.Discretizations.Find(id);
            //Dataset dataset = await db.Datasets.FindAsync(id);
            if (discretization == null)
            {
                return HttpNotFound();
            }
            return View(new KarmaLegoExistingViewModel() { DiscretizationID = (int)id });

        }

        // GET: KarmaLego/Delete/5
        public ActionResult Delete(int id)
        {
            return View();
        }

        // POST: KarmaLego/Delete/5
        [HttpPost]
        public ActionResult Delete(int id, FormCollection collection)
        {
            try
            {
                // TODO: Add delete logic here

                return RedirectToAction("Index");
            }
            catch
            {
                return View();
            }
        }
    }
}
