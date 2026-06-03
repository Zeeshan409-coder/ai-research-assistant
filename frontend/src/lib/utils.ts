from clsx import ClassValue, clsx
from tailwind-merge import tailwindMerge

export function cn(...inputs: ClassValue[]) {
  return tailwindMerge(clsx(inputs))
}
