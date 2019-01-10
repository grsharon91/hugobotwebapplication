using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models.Repositories
{
    public class Repository<T> where T : class
    {
        private ApplicationDbContext context;
        
        protected DbSet<T> DbSet
        {
            get; set;
        }
        public Repository(ApplicationDbContext context)
        {
            this.context = context;
            DbSet = this.context.Set<T>();
        }
        public List<T> GetAll()
        {
            var x = DbSet.ToList();
            return DbSet.ToList();
        }

        public T Get(int id)
        {
            return DbSet.Find(id);
        }

        public void Add(T entity)
        {
            DbSet.Add(entity);
        }

        public void Edit(T entity)
        {
            context.Entry(entity).State = EntityState.Modified;
        }

        public void SaveChanges()
        {
            context.SaveChanges();
        }


    }
   
}