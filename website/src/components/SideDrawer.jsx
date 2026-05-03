import { AnimatePresence, motion } from "framer-motion";
import { ArrowUpRight, X } from "lucide-react";

function SideDrawer({ open, onClose, groups }) {
  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.button
            className="drawer-backdrop"
            aria-label="Close menu"
            type="button"
            onClick={onClose}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          />
          <motion.aside
            className="side-drawer"
            initial={{ x: -420, opacity: 0.8 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -420, opacity: 0 }}
            transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="flex items-start justify-between gap-6">
              <div>
                <p className="eyebrow">Invoice Automation</p>
                <h2 className="mt-2 text-2xl font-semibold tracking-tight text-stone-950">
                  Workspace menu
                </h2>
              </div>
              <button className="icon-button" type="button" onClick={onClose} aria-label="Close drawer">
                <X size={20} />
              </button>
            </div>

            <div className="mt-10 space-y-8">
              {groups.map((group) => (
                <div key={group.title}>
                  <p className="drawer-title">{group.title}</p>
                  <div className="mt-3 space-y-1">
                    {group.items.map((item) => (
                      item.disabled ? (
                        <span className="drawer-link cursor-not-allowed opacity-60" key={`${group.title}-${item.label}`}>
                          <span>{item.label}</span>
                          <span className="text-xs uppercase tracking-[0.18em] text-stone-400">TODO</span>
                        </span>
                      ) : (
                        <a
                          className="drawer-link"
                          href={item.href}
                          key={`${group.title}-${item.label}`}
                          onClick={onClose}
                          rel="noreferrer"
                          target={item.href?.startsWith("http") ? "_blank" : undefined}
                        >
                          <span>{item.label}</span>
                          <ArrowUpRight size={15} />
                        </a>
                      )
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}

export default SideDrawer;
