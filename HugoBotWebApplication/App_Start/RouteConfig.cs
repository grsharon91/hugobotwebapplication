using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Routing;

namespace HugoBotWebApplication
{
    public class RouteConfig
    {
        public static void RegisterRoutes(RouteCollection routes)
        {
            routes.IgnoreRoute("{resource}.axd/{*pathInfo}");

			routes.MapRoute(
				name: "Default",
				url: "{controller}/{action}",
				defaults: new { controller = "Home", action = "Index" }
			);
			//routes.MapRoute(
			//  name: "Home",
			//  url: "",
			//  defaults: new { controller = "Home", action = "Index", id = UrlParameter.Optional }
			// );
			//  routes.MapRoute(
			//  name: "FirstSteps",
			//  url: "FirstSteps",
			//  defaults: new { controller = "Home", action = "FirstSteps", id = UrlParameter.Optional }
			// );
			//routes.MapRoute(
			//         name: "About",
			//         url: "About",
			//         defaults: new { controller = "Home", action = "About", id = UrlParameter.Optional }
			//     );
			//         routes.MapRoute(
			//         name: "Contact",
			//         url: "Contact",
			//         defaults: new { controller = "Home", action = "Contact", id = UrlParameter.Optional }
			//     );
			//         routes.MapRoute(
			//         name: "Register",
			//         url: "Register",
			//         defaults: new { controller = "Account", action = "Register", id = UrlParameter.Optional }
			//     );
			//         routes.MapRoute(
			//         name: "Login",
			//         url: "Login",
			//         defaults: new { controller = "Account", action = "Login", id = UrlParameter.Optional }
			//     );
			//        routes.MapRoute(
			//         name: "LogOff",
			//         url: "LogOff",
			//         defaults: new { controller = "Account", action = "LogOff", id = UrlParameter.Optional }
			//     );
			//         routes.MapRoute(
			//            name: "Datasets",
			//            url: "Datasets",
			//            defaults: new { controller = "Datasets", action = "Index", id = UrlParameter.Optional }
			//        );

			// routes.MapRoute(
			//   name: "OwnedDatasets",
			//   url: "OwnedDatasets",
			//   defaults: new { controller = "Datasets", action = "OwnedDatasets", id = UrlParameter.Optional }
			//  );
			//routes.MapRoute(
			//             name: "DatasetsUpload",
			//             url: "DatasetUpload",
			//             defaults: new { controller = "Datasets", action = "Create", id = UrlParameter.Optional }
			//         );
			//         routes.MapRoute(
			//            name: "DiscretizationUpload",
			//            url: "Discret5izationUpload",
			//            defaults: new { controller = "Discretizations", action = "Create", id = UrlParameter.Optional }
			//        );
			//         routes.MapRoute(
			//            name: "DatasetsDownload",
			//            url: "Download/{id}",
			//            defaults: new { controller = "Datasets", action = "Download", id = UrlParameter.Optional }
			//        );

			//routes.MapRoute(
			// name: "ProccessFile",
			// url: "Datasets/ProcessFile",
			// defaults: new { controller = "Datasets", action = "ProcessFile", id = UrlParameter.Optional }
			//);

			routes.MapRoute(
					 name: "DatasetsDownloadFiles",
					 url: "Datasets/DownloadFiles/{*parameters}",
					 defaults: new { controller = "Datasets", action = "DownloadFiles", parameters = UrlParameter.Optional }
				 );

			routes.MapRoute(
					 name: "DiscretizationsDownloadFiles",
					 url: "Discretizations/GetDiscretizations/{*parameters}",
					 defaults: new { controller = "Discretizations", action = "GetDiscretizations", parameters = UrlParameter.Optional }
				 );

			//         routes.MapRoute(
			//          name: "DatasetsEdit",
			//          url: "Edit/{id}",
			//          defaults: new { controller = "Datasets", action = "Edit", id = UrlParameter.Optional }
			//      );
			//         routes.MapRoute(
			//         name: "ViewMetadata",
			//         url: "ViewMetadata/{id}",
			//         defaults: new { controller = "Datasets", action = "DisplayMetadata", id = UrlParameter.Optional }
			//     );

			//         routes.MapRoute(
			//         name: "SaveMetaData",
			//         url: "Datasets/SaveMetaData/{datasetId}",
			//         defaults: new { controller = "Datasets", action = "SaveMetaData", datasetId = UrlParameter.Optional }
			//     );

			//         routes.MapRoute(
			//               name: "KarmaLegoUpload",
			//               url: "KarmaLegoUpload",
			//               defaults: new { controller = "KarmaLego", action = "Create", id = UrlParameter.Optional }
			//     );
			//         routes.MapRoute(
			//      name: "KarmaLegoEdit",
			//      url: "KarmaLego/Edit/{id}",
			//      defaults: new { controller = "KarmaLego", action = "Edit", id = UrlParameter.Optional }
			//  );

		}
    }
}
