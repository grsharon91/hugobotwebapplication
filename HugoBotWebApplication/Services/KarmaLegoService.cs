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

		//public List<Discretization> CreateDiscretizationsFromKarmaLegoViewModel(KarmaLegoViewModel karmaLegoViewModel)
		//{
		//	List<Discretization> discretizations = new List<Discretization>();

		//	//discretization.DatasetID = lastDatasetID + 1;
		//	SetParametersForDataset(karmaLegoViewModel, discretizations);
		//	return discretizations;

		//}
	}
}