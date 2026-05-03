import { motion } from "framer-motion";

const reveal = {
  hidden: { opacity: 0, y: 26 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.65, ease: [0.22, 1, 0.36, 1] },
  },
};

function MotionSection({ children, className = "", id }) {
  return (
    <motion.section
      className={className}
      id={id}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.16 }}
      variants={reveal}
    >
      {children}
    </motion.section>
  );
}

export default MotionSection;
