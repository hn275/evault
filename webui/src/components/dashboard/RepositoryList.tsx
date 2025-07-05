import { RepositoryCard } from "./RepositoryCard";
import type { Repository } from "../../types/Repository";
import { motion } from "motion/react";

export function RepositoryList({
  repositories,
}: {
  repositories: Repository[];
}) {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.05, // Stagger each card by 50ms (really fast)
      },
    },
  };

  const itemVariants = {
    hidden: { 
      opacity: 0, 
      y: 20 // Start 20px down
    },
    visible: { 
      opacity: 1, 
      y: 0
    },
  };

  return (
    <motion.div
      className="flex flex-col gap-1 mt-4"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {repositories.map((repo) => (
        <motion.div
          key={repo.id}
          variants={itemVariants}
        >
          <RepositoryCard repo={repo} />
        </motion.div>
      ))}
    </motion.div>
  );
}
