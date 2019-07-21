using HugoBotWebApplication.Models;
using HugoBotWebApplication.ViewModels;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Web;

namespace HugoBotWebApplication.Services
{
	public class KarmaLegoService
	{
		public KarmaLego CreateDiscretizationsFromKarmaLegoExistingViewModel(KarmaLegoExistingViewModel karmaLegoExistingViewModel)
		{
			KarmaLego karmaLego = new KarmaLego
			{
				Epsilon = karmaLegoExistingViewModel.Epsilon,
				MaximumGap = karmaLegoExistingViewModel.MaximumGap,
				MinimumVerticalSupport = karmaLegoExistingViewModel.MinimumVerticalSupport,
				Visibility = karmaLegoExistingViewModel.Visibility,
				IsReady = "In Progress",
			};
			
			return karmaLego;
		}

		public string getParams(KarmaLego kl)
		{
			return String.Join("/", new[] { "KarmaLego", String.Join("_", new[] { kl.Epsilon.ToString(), kl.MaximumGap.ToString(), kl.MinimumVerticalSupport.ToString() }) });
		}

        // get the classes by the files in the karmaLego output - the name file is TIRPS_DISCERIZED_CLASSx
        public string [] getClasses(string path)
        {
            string fullPath = Path.Combine(HttpRuntime.AppDomainAppPath, path);
            string[] files = System.IO.Directory.GetFiles(fullPath);
            List<string> classes = new List<string>();
            foreach (string f in files)
            {
                string[] split = f.Split('_');
                // get the "classx.csv" and remove the .csv 
                string tmp = split[split.Length - 1];
                tmp = tmp.Substring(0, tmp.Length - 4);
                classes.Add(tmp);
            }
            //return array["class0", "class1" , ...]
            return classes.ToArray();
        }

        public void sendToKL(string inputPath, string outputPath, double epsilon, double minVerticalSupport, int maxGap)
        {
            Directory.CreateDirectory(Path.Combine(HttpRuntime.AppDomainAppPath, outputPath));
            CmdService cmd = new CmdService();
            string cli = "python KarmaLegoRunner.py " + inputPath + " " + outputPath + " " + epsilon.ToString() + " " + minVerticalSupport.ToString() + " " + maxGap.ToString();
            Task task = cmd.SendToCMD(cli, "HugobotKarmaLegoRunner");
        }

        public string getPath (string discPath, int id)
        {
            string path = discPath + "/KarmaLego/" + id.ToString();
            return path;
        }

        //public List<Discretization> CreateDiscretizationsFromKarmaLegoViewModel(KarmaLegoViewModel karmaLegoViewModel)
        //{
        //	List<Discretization> discretizations = new List<Discretization>();

        //	//discretization.DatasetID = lastDatasetID + 1;
        //	SetParametersForDataset(karmaLegoViewModel, discretizations);
        //	return discretizations;

        //}
    }
}