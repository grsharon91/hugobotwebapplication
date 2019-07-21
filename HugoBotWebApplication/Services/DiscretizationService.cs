using HugoBotWebApplication.CommunicationLayer;
using HugoBotWebApplication.Models;
using HugoBotWebApplication.ViewModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.IO;
using System.Threading.Tasks;
using static HugoBotWebApplication.Utils.Settings;
namespace HugoBotWebApplication.Services
{
    public class DiscretizationService
    {
        private List<string> taskCompleated = new List<string>();
        private readonly List<string> methodsWithParameters = new List<string> { "TD4C", "EXPERT", "SAX" };
        private readonly FileTransferrer fileTransferrer = new FileTransferrer();
        public bool isDone = false;
        private string FormatParams(string methodName, List<string> methodParameters)
        {
            string formattedParams = MethodEncodingToMethodName[methodName] + "$" + methodName;
            foreach (var methodParam in methodParameters)
            {
                formattedParams = formattedParams + "_" + methodParam;
            }
            return ";" + formattedParams;
        }

	

        public string GetDownloadPath(List<Discretization> discretizations)
        {
            List<string> downloadPath = new List<string>();
            foreach (Discretization discretization in discretizations)
                downloadPath.Add(discretization.DownloadPath);

            return String.Join(" ", downloadPath);
        }

        public List<Discretization> CreateDiscretizations(Dataset dataset,string[] methodsList, int id, string datasetPath)
        {
            List<Discretization> discretizations = new List<Discretization>();
            for (int i = 0; i < methodsList.Length; i++)
            {
               // Directory.CreateDirectory(Path.Combine(HttpRuntime.AppDomainAppPath, getPath(datasetPath, id) + @"\KarmaLego"));
                List<string> methodParameters = methodsList[i].Split('/')[1].Split('_').ToList();
                string methodName = methodsList[i].Split('/')[0];
                if ( DistanceMeasureMethods.Contains(methodName))
                {
                    int binsNumber = Int32.Parse(methodParameters[0]);
                    string distanceMeasure = methodParameters[1];
                    int maxGap = Int32.Parse(methodParameters[2]);
                    int windowSize = Int32.Parse(methodParameters[3]);
                    methodsList[i] = datasetPath + "/" + methodName + "/" + String.Join("_", methodParameters);
                    DistanceMeasureDescritization d = new DistanceMeasureDescritization()
                    {
                        DiscretizationID = id,
                        Dataset = dataset,
                        DownloadPath = methodsList[i],
                        Visibility = "",
                        Type = "Discretized",
                        FullName = MethodEncodingToMethodName[methodName],
                        ParametersIsReady = "In Progress",
                        BinsNumber = binsNumber,
                        MaxGap = maxGap,
                        WindowSize = windowSize
                    };
                    discretizations.Add(d);
                }
                else
                {
                    int binsNumber = Int32.Parse(methodParameters[0]);
                    int maxGap = Int32.Parse(methodParameters[1]);
                    int windowSize = Int32.Parse(methodParameters[2]);
                    //string path = dataset.Path.Substring(0, dataset.Path.Length - 4) + "/discretizations/" + getFullMethodName(methodName, "") + "_" + binsNumber + "bins_" + windowSize + "paa_" + maxGap + "max-gap";
                    string outputPath = datasetPath + @"/Discretizations" + id.ToString();
                    Discretization d = new Discretization()
                    {
                        DiscretizationID = id,
                        Dataset = dataset,
                        DownloadPath = outputPath,
                        Visibility = "",
                        Type = "Discretized",
                        FullName = MethodEncodingToMethodName[methodName],
                        ParametersIsReady = "In Progress",
                        BinsNumber = binsNumber,
                        MaxGap = maxGap,
                        WindowSize = windowSize
                    };
                    discretizations.Add(d);

                }


            }
            return discretizations;
        }

        public string Discretize(string[] methodsList, string path, int id)
        {
            path = path.Substring(2, path.Length-2);
            string fullPath = Path.Combine(HttpRuntime.AppDomainAppPath, path);
            string outputPath = getPath(fullPath, id);
            Directory.CreateDirectory(outputPath);
            string[] fileName = Directory.GetFiles(fullPath);
            fullPath = fileName[0];
            for (int i = 0; i < methodsList.Length; i++)
            {
                List<string> methodParameters = methodsList[i].Split('/')[1].Split('_').ToList();
                string methodName = methodsList[i].Split('/')[0];
                    string binsNumber = methodParameters[0];
                    string maxGap = methodParameters[1];
                    string windowSize = methodParameters[2];
                    CmdService cmd = new CmdService();

                if (DistanceMeasureMethods.Contains(methodName))
                {
                    binsNumber = methodParameters[0];
                    string distanceMeasure = methodParameters[1];
                    maxGap = methodParameters[2];
                    windowSize = methodParameters[3];
                    methodName = getFullMethodName(methodName, distanceMeasure);
                }
                else
                {
                    methodName = getFullMethodName(methodName, "");
                }
                
                string cli = "python cli.py temporal-abstraction " + fullPath + " " + outputPath + " per-dataset -paa " + windowSize + " " + maxGap + " discretization " + methodName + " " + binsNumber;
                Task task = cmd.SendToCMD(cli, "DiscretizationRunner");
                
            }

            return "Success";
        }


        public string getPath(string datasetPath, int discretizationId)
        {
            string path = datasetPath + "/Discretizations/" + discretizationId.ToString();
            return path;
        }

        private string getFullMethodName(string name, string distanceMeasure)
        {
            string fullName = "";
            if (DistanceMeasureMethods.Contains(name))
            {
                switch (distanceMeasure)
                {
                    case "Cosine":
                        fullName = "td4c-cosine";
                        break;
                    case "Entropy":
                        fullName = "td4c-entropy";
                        break;
                    case "KullbackLiebler":
                        fullName = "td4c-skl";
                        break;
                }
            }
            else
            {
                switch (name)
                {
                    case "EQW":
                        fullName = "equal-width";
                        break;

                    case "EQF":
                        fullName = "equal-frequency";
                        break;
                    case "SAX":
                        fullName = "sax";
                        break;
                    case "PERSIST":
                        fullName = "persist";
                        break;
                    case "KMEANS":
                        fullName = "kmeans";
                        break;
                }
            }

            return fullName;
        }
	
	}
}
