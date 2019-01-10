using HugoBotWebApplication.CommunicationLayer;
using HugoBotWebApplication.Models;
using HugoBotWebApplication.ViewModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using static HugoBotWebApplication.Utils.Settings;
namespace HugoBotWebApplication.Services
{
    public class DiscretizationService
    {
        private readonly List<string> methodsWithParameters = new List<string> { "TD4C", "EXPERT", "SAX" };
        private readonly FileTransferrer fileTransferrer = new FileTransferrer();
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
                    methodsList[i] = dataset.Path + "/" + methodName + "/" + String.Join("_", methodParameters);
                    Discretization d = new Discretization()
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


            }
            return discretizations;
        }

        public string Discretize(string[] methodsList)
        {
            fileTransferrer.DescretizeDataset(String.Join(" ", methodsList));
            return "Success";
        }


	
	}
}
