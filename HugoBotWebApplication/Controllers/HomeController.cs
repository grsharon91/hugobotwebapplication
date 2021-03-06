﻿using HugoBotWebApplication.Models;
using HugoBotWebApplication.ViewModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Microsoft.AspNet.Identity;
namespace HugoBotWebApplication.Controllers
{
    public class HomeController : Controller
    {
        private ApplicationDbContext db = new ApplicationDbContext();

        public ActionResult Index()
        {
            string currentUserId = null;
            List<ViewPermissions> vpList = new List<ViewPermissions>();
            if (User != null && User.Identity != null)
            {
                currentUserId = User.Identity.GetUserId();
            }

            if (currentUserId != null)
            {
                ApplicationUser user = db.Users.Find(currentUserId);
                if (!user.EmailConfirmed)
                    ViewBag.Confirm = "Dear " + user.FirstName + " " + user.LastName + ", Please confirm your email address and wait for us to confirm your email in order to perform actions in the website. We thank you for your patience.";


                string name = user.UserName;
                var viewPermissions = db.ViewPermissions.Where(u => u.UserName == name);
                foreach (ViewPermissions vp in viewPermissions)
                {
                    vpList.Add(vp);
                }
            }
            DatasetIndexViewModel datasetIndexViewModel = new DatasetIndexViewModel()
            {
                Datasets = db.Datasets.ToList(),
                ViewPermissionsRecords = vpList
            };


            return View(datasetIndexViewModel);
        }

        public ActionResult FirstSteps()
        {
            return View();
        }
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
    }
}
