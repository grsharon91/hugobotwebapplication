using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Data.Entity;
using System.Security.Claims;
using System.Security.Principal;
using System.Threading.Tasks;
using System.Web;
using Microsoft.AspNet.Identity;
using Microsoft.AspNet.Identity.EntityFramework;
using Microsoft.AspNet.Identity.Owin;

namespace HugoBotWebApplication.Models
{
    // You can add profile data for the user by adding more properties to your ApplicationUser class, please visit https://go.microsoft.com/fwlink/?LinkID=317594 to learn more.
    public class ApplicationUser : IdentityUser
    {
        public bool IsAuthorized;
        public string FirstName { get; set; }
		public string LastName { get; set; }
		public string Institute { get; set; }
		public string Degree { get; set; }
        public bool OwnConfirmation { get; set; }

		[InverseProperty("Users")]
		public virtual List<UserGroup> Groups { get; set; }
		[InverseProperty("Owner")]
		public virtual List<UserGroup> OwnedGroups { get; set; }
		public virtual List<Dataset> OwnedDatasets { get; set; }
        public virtual List<Discretization> OwnedDiscretizations { get; set; }
        public virtual List<KarmaLego> OwnedKarmaLegos { get; set; }
        public async Task<ClaimsIdentity> GenerateUserIdentityAsync(UserManager<ApplicationUser> manager)
        {
            // Note the authenticationType must match the one defined in CookieAuthenticationOptions.AuthenticationType
            var userIdentity = await manager.CreateIdentityAsync(this, DefaultAuthenticationTypes.ApplicationCookie);
			// Add custom user claims here
			userIdentity.AddClaim(new Claim("FirstName", this.FirstName));
			userIdentity.AddClaim(new Claim("LastName", this.LastName));

			return userIdentity;
        }
    }

	public static class IdentityHelper
	{

		public static string GetFirstName(this IIdentity identity)
		{
			var claim = ((ClaimsIdentity)identity).FindFirst("FirstName");
			// Test for null to avoid issues during local testing
			return (claim != null) ? claim.Value : string.Empty;
		}

		public static string GetLastName(this IIdentity identity)
		{
			var claim = ((ClaimsIdentity)identity).FindFirst("LastName");
			// Test for null to avoid issues during local testing
			return (claim != null) ? claim.Value : string.Empty;
		}
	}

	public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
    {
        public System.Data.Entity.DbSet<HugoBotWebApplication.Models.Dataset> Datasets { get; set; }
        public System.Data.Entity.DbSet<HugoBotWebApplication.Models.Discretization> Discretizations{ get; set; }
        public System.Data.Entity.DbSet<HugoBotWebApplication.Models.DistanceMeasureDescritization> DistanceMeasureDiscretizations { get; set; }
        public System.Data.Entity.DbSet<HugoBotWebApplication.Models.KarmaLego> KarmaLegos { get; set; }
        public System.Data.Entity.DbSet<HugoBotWebApplication.Models.TempDataset> TempDatasets{ get; set; }
        public System.Data.Entity.DbSet<HugoBotWebApplication.Models.TempDiscretization> TempDiscretizations{ get; set; }
        public System.Data.Entity.DbSet<HugoBotWebApplication.Models.ViewPermissions> ViewPermissions { get; set; }

        public ApplicationDbContext()
            : base("ApplicationDbContext", throwIfV1Schema: false)
        {
           
        }

    
        public static ApplicationDbContext Create()
        {
            return new ApplicationDbContext();
        }
    }
}