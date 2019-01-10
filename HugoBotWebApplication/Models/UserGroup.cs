using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models
{
	public class UserGroup
	{
		public int UserGroupId { get; set; }
		public virtual List<ApplicationUser> Users{ get; set;}
		public string GroupName { get; set; }
		public string OwnerId { get; set; }
		public virtual ApplicationUser Owner { get; set; }
	}
}