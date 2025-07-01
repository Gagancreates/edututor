import type { LucideIcon } from "lucide-react"
import * as LucideIcons from "lucide-react"

interface FeatureCardProps {
  icon: string
  title: string
  description: string
  color: string
}

export default function FeatureCard({ icon, title, description, color }: FeatureCardProps) {
  // Dynamically get the icon component
  const IconComponent = LucideIcons[icon as keyof typeof LucideIcons] as LucideIcon

  return (
    <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
      <div
        className="size-14 rounded-xl flex items-center justify-center mb-5"
        style={{ backgroundColor: `${color}15` }}
      >
        <IconComponent style={{ color }} className="h-7 w-7" />
      </div>
      <h3 className="font-satoshi font-bold text-xl mb-3">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}
