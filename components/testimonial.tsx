import Image from "next/image"
import { Quote } from "lucide-react"

interface TestimonialProps {
  quote: string
  author: string
  role: string
  avatar: string
}

export function Testimonial({ quote, author, role, avatar }: TestimonialProps) {
  return (
    <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
      <Quote className="h-8 w-8 text-[#4ECDC4] mb-4 opacity-50" />
      <p className="text-gray-700 mb-6 text-lg">{quote}</p>
      <div className="flex items-center">
        <div className="mr-4">
          <Image src={avatar || "/placeholder.svg"} alt={author} width={50} height={50} className="rounded-full" />
        </div>
        <div>
          <p className="font-satoshi font-bold">{author}</p>
          <p className="text-gray-500 text-sm">{role}</p>
        </div>
      </div>
    </div>
  )
}
