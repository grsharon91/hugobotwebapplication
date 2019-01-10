using System;
using System.Collections.Generic;
using System.Web;
using System.Web.Mvc;
using Newtonsoft.Json;
using HugoBotWebApplication.Services;
using System.IO;
using System.Text;
using HugoBotWebApplication.Models;
using HugoBotMVC.Services;
using Microsoft.AspNet.Identity;
namespace HugoBotMVC.Controllers
{
    public class KarmaLegoVController : Controller
    {
        public LegoObjects.LegoResults curResults;
        public byte[] indexFileAsByteArr;
        private ApplicationDbContext db = new ApplicationDbContext();

        public ActionResult Index()
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

        public ActionResult MergedIndex()
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

        [HttpPost]
        public void loadFiles()
        {
            StatesConverter cnvLabels;
            EntitiesData datEnts;

            try
            {
                var ft = new HugoBotWebApplication.Discretistation.FileHandler(); 
                string pathWithClass = Session["correntPathToIndex"].ToString();
                var ansFromGetChunks = ft.GetChunks(pathWithClass); // we don't use this data, this is just init for chunk creation
                TestMemory._chunkesLargerThanZero = new List<string>(ansFromGetChunks);

                // ask for index file
                pathWithClass += "/index";
                indexFileAsByteArr = ft.GetChunk(pathWithClass); // ask for index file

                // ask for entities file
                string datasetGUID = ((Dataset)Session["dataset"]).Path;
                byte[] entitiesByteArr = ft.GetFile(datasetGUID + "/entities");

                // ask for states file
                string pathWithDiscConfig = (string)Session["discConfig"];
                string pathToState = pathWithDiscConfig + "/states";
                byte[] statesByteArr = ft.GetStates(pathToState);

                // load states file
                cnvLabels = new StatesConverter(statesByteArr);

                // load enetites file
                datEnts = new EntitiesData(entitiesByteArr);


                // create curResultsObject
                LoadLegoResultsDataset(indexFileAsByteArr, cnvLabels, datEnts);

                // assiggn curResult to class that not goint to be deleted after uploading
                TestMemory.curResults = this.curResults;

                TestMemory.index = getIndex();
            }
            catch(Exception ex)
            {
                var axax = 1;
            }
        }

        [HttpPost]
        public ContentResult getSubTree() // (string chunkName)
        {
            string answerString = "";

            try
            {
                string isMergedString = Request.Form["isMerged"];
                bool isMerged = false;
                if (isMergedString == "true")
                    isMerged = true;
                string porpName = Request.Form["propertyName"];
                var ft = new HugoBotWebApplication.Discretistation.FileHandler();

                string pathToChunk = Session["correntPathToIndex"].ToString() + "/" + porpName;
                byte[] chuckAsByteArr = ft.GetChunk(pathToChunk);

                var answer = Data.loadKarmaSubTree(chuckAsByteArr, isMerged);
                answerString = JsonConvert.SerializeObject(answer, Formatting.Indented);
            }
            catch(Exception ex)
            {
                var xs = 124124;
            }

            return Content(answerString);
        }

        public JsonResult getEntites()
        {
            var answer = new
            {
                header = new List<string>(),
                rows = new List<List<string>>()
            };

            try
            {
                string dataPath = ((Dataset)Session["dataset"]).Path;
                var ft = new HugoBotWebApplication.Discretistation.FileHandler();
                byte[] b = ft.GetFile(dataPath + "/entities");

                using (StreamReader reader = new StreamReader(new MemoryStream(b), Encoding.Default))
                {
                    // get and set attributes names
                    var line = reader.ReadLine();
                    var values = line.Split(',');

                    foreach (string attributeName in values)
                    {
                        answer.header.Add(attributeName);
                    }

                    int indexLine = 0;
                    while (reader.EndOfStream == false)
                    {
                        answer.rows.Add(new List<string>());
                        var splits = reader.ReadLine().Split(',');
                        for (int i = 0; i < splits.Length; i++) // 1 for skipping the id Column
                        {
                            string valueToEnter = splits[i];
                            answer.rows[indexLine].Add(valueToEnter);
                        }
                        indexLine++;
                    }
                }
            }
            catch { }
            return Json(answer, JsonRequestBehavior.AllowGet);
        }


        [HttpGet]
        public ContentResult getMetadata()
        {
            string resAsJson = "";
            try
            {
                var res = new
                {
                    TestMemory.curResults.CurrentLevel,
                    TestMemory.curResults.Root,
                    dictState = TestMemory.curResults.cnvLabels.getDicStates(),
                    datEntities = TestMemory.curResults.datEntities.getData(),
                    cutPropertiesPath = TestMemory.curResults.curPropertiesPath,
                    chunkesLargerThanZero = TestMemory._chunkesLargerThanZero,
                    TestMemory.index
                };
                resAsJson = JsonConvert.SerializeObject(res);
            }
            catch { }
            return Content(resAsJson);
        }


        [HttpGet]
        public ContentResult getRootElements()
        {
            string resAsJson = "";

            try
            {
                var res = new
                {
                    TestMemory.curResults.RootElements,
                };
                resAsJson = JsonConvert.SerializeObject(res);
            }
            catch { }

            return Content(resAsJson);
        }

        private void LoadLegoResultsDataset(byte[] chunkByteArr, StatesConverter cnv, EntitiesData datEnts)
        {
            // Alon: please dont remove this comments. We need that for in order to add support in more formats

            /*
            if (Methods.getFileNameExtension(indexFileName).ToLower() == "xml")
                this.curResults = new LegoObjects.LegoResults(Data.getRoot(indexFileName), cnv, datEnts);
            else if (Methods.getFileNameExtension(indexFileName).ToLower() == "karma")
                this.curResults = new LegoObjects.LegoResults(indexFile.InputStream, cnv, datEnts);
            else // invalid wekamatrixfile name */
            this.curResults = new LegoObjects.LegoResults(chunkByteArr, cnv, datEnts);
            return;
        }

        public object[] getIndex()
        {
            List<object> l = new List<object>();

            try
            {
                string correntPath = Session["correntPathToIndex"].ToString();

                var ft = new HugoBotWebApplication.Discretistation.FileHandler();

                var ansFromGetChunks = ft.GetChunks(correntPath);

                correntPath += "/index";
                var indexBeforeParse = ft.GetChunk(correntPath);

                l = FileConvertor.parseByteArrToIndex(indexBeforeParse);
            }
            catch { }
            return l.ToArray();
        }

        private void LoadRootLevel()
        {
            // Alon: need to check in oroginal project
            return;
        }

        #region about and contact
        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
        #endregion
    } // class
} // namespace