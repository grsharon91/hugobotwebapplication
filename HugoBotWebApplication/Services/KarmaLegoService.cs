using HugoBotWebApplication.Models;
using HugoBotWebApplication.ViewModels;
using System;
using System.Collections.Generic;
using System.Linq;
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
            string fullPath = HttpContext.Current.Server.MapPath(path);
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

		//public List<Discretization> CreateDiscretizationsFromKarmaLegoViewModel(KarmaLegoViewModel karmaLegoViewModel)
		//{
		//	List<Discretization> discretizations = new List<Discretization>();

		//	//discretization.DatasetID = lastDatasetID + 1;
		//	SetParametersForDataset(karmaLegoViewModel, discretizations);
		//	return discretizations;

		//}
	}
}