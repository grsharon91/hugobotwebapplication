using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Entity;
using System.Linq;
using System.Threading.Tasks;
using System.Net;
using System.Web;
using System.Web.Mvc;
using HUGO_BOT.Models;

namespace HUGO_BOT.Controllers
{
    public class DummiesController : Controller
    {
        private HUGO_BOTContext db = new HUGO_BOTContext();

        // GET: Dummies
        public async Task<ActionResult> Index()
        {
            return View(await db.Dummies.ToListAsync());
        }

        // GET: Dummies/Details/5
        public async Task<ActionResult> Details(int? id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            Dummy dummy = await db.Dummies.FindAsync(id);
            if (dummy == null)
            {
                return HttpNotFound();
            }
            return View(dummy);
        }

        // GET: Dummies/Create
        public ActionResult Create()
        {
            return View();
        }

        // POST: Dummies/Create
        // To protect from overposting attacks, please enable the specific properties you want to bind to, for 
        // more details see https://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> Create([Bind(Include = "DummyID,MyProperty")] Dummy dummy)
        {
            if (ModelState.IsValid)
            {
                db.Dummies.Add(dummy);
                await db.SaveChangesAsync();
                return RedirectToAction("Index");
            }

            return View(dummy);
        }

        // GET: Dummies/Edit/5
        public async Task<ActionResult> Edit(int? id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            Dummy dummy = await db.Dummies.FindAsync(id);
            if (dummy == null)
            {
                return HttpNotFound();
            }
            return View(dummy);
        }

        // POST: Dummies/Edit/5
        // To protect from overposting attacks, please enable the specific properties you want to bind to, for 
        // more details see https://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> Edit([Bind(Include = "DummyID,MyProperty")] Dummy dummy)
        {
            if (ModelState.IsValid)
            {
                db.Entry(dummy).State = EntityState.Modified;
                await db.SaveChangesAsync();
                return RedirectToAction("Index");
            }
            return View(dummy);
        }

        // GET: Dummies/Delete/5
        public async Task<ActionResult> Delete(int? id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            Dummy dummy = await db.Dummies.FindAsync(id);
            if (dummy == null)
            {
                return HttpNotFound();
            }
            return View(dummy);
        }

        // POST: Dummies/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> DeleteConfirmed(int id)
        {
            Dummy dummy = await db.Dummies.FindAsync(id);
            db.Dummies.Remove(dummy);
            await db.SaveChangesAsync();
            return RedirectToAction("Index");
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                db.Dispose();
            }
            base.Dispose(disposing);
        }
    }
}
