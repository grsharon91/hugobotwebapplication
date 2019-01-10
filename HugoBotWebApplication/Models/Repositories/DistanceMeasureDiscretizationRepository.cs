using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models.Repositories
{
    public class DistanceMeasureDiscretizationRepository : Repository<DistanceMeasureDescritization>
    {
        public DistanceMeasureDiscretizationRepository(ApplicationDbContext context) : base(context)
        {

        }
    }
}