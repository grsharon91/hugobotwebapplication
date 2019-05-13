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

        public List<Discretization> CreateDiscretizations(Dataset dataset,string[] methodsList)
        {
            List<Discretization> discretizations = new List<Discretization>();
            for (int i = 0; i < methodsList.Length; i++)
            {   
                List<string> methodParameters = methodsList[i].Split('/')[1].Split('_').ToList();
                string methodName = methodsList[i].Split('/')[0];
                if ( DistanceMeasureMethods.Contains(methodName))
                {
                    int binsNumber = Int32.Parse(methodParameters[0]);
                    string distanceMeasure = methodParameters[1];
                    int maxGap = Int32.Parse(methodParameters[2]);
                    int windowSize = Int32.Parse(methodParameters[3]);
                    methodsList[i] = dataset.Path + "/" + methodName + "/" + String.Join("_", methodParameters);
                    DistanceMeasureDescritization d = new DistanceMeasureDescritization()
                    {
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
                    string path = dataset.Path.Substring(0, dataset.Path.Length - 4) + "/discretizations/" + getFullMethodName(methodName, "") + "_" + binsNumber + "bins_" + windowSize + "paa_" + maxGap + "max-gap";
                    //string fullPath = HttpContext.Current.Server.MapPath(path);
                    //methodsList[i] = dataset.Path + "/" + methodName + "/" + String.Join("_", methodParameters);
                    Discretization d = new Discretization()
                    {
                        Dataset = dataset,
                        DownloadPath = path,
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

        public string Discretize(string[] methodsList, string path)
        {
            string fullPath = HttpContext.Current.Server.MapPath(path);
       //    List<Discretization> discretizations = new List<Discretization>();
            for (int i = 0; i < methodsList.Length; i++)
            {
                List<string> methodParameters = methodsList[i].Split('/')[1].Split('_').ToList();
                string methodName = methodsList[i].Split('/')[0];
                    string binsNumber = methodParameters[0];
                //    string distanceMeasure = methodParameters[1];
                    string maxGap = methodParameters[1];
                    string windowSize = methodParameters[2];
                    // fileTransferrer.DescretizeDataset(String.Join(" ", methodsList));
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
                
                string outputPath = fullPath.Substring(0, fullPath.Length - 4) + "\\discretizations";
                if (!Directory.Exists(outputPath))
                    Directory.CreateDirectory(outputPath);
                string cli = "python cli.py discretize -i " + fullPath +  " -o " + outputPath + " -pw " + windowSize + " -g " + maxGap + " dataset " + methodName +" " + binsNumber;
                Task task = cmd.SendToDiscretization(cli, isDone);
                //if (task.IsCompleted)
                //{
                //    taskCompleated[i] = "Ready";
                //}
                //else
                //{
                //    //taskCompleated[i] = "In Progress";

                //}
                
            }

            return "Success";
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
