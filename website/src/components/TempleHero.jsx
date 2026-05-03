import { motion } from "framer-motion";
import templeHero from "../assets/temple-hero.png";

function TempleHero() {
  return (
    <motion.div
      className="temple-stage"
      initial={{ opacity: 0, scale: 0.96, y: 18 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1] }}
    >
      <div className="temple-glow" />
      <img
        src={templeHero}
        alt="Premium 3D temple visual used as an AI product anchor"
        className="temple-image"
      />
    </motion.div>
  );
}

export default TempleHero;
