import { motion } from "framer-motion";

function PremiumCard({ children, className = "", as = "article" }) {
  const Component = motion[as] || motion.article;

  return (
    <Component
      className={`premium-card ${className}`}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.28, ease: "easeOut" }}
    >
      {children}
    </Component>
  );
}

export default PremiumCard;
