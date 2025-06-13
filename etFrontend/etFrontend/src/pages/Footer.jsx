import React from 'react'

function Footer() {
  return (
    <div className=''>
      

<footer className="bg-gray-900 shadow-sm dark:bg-gray-900 mt-5">
    <div className="container max-w-5xl mx-auto px-4 md:py-8">
        <div className="sm:flex sm:items-center sm:justify-between">
            <a href="https://flowbite.com/" className="flex items-center mb-4 sm:mb-0 space-x-3 rtl:space-x-reverse">
                <span className="self-center text-2xl font-semibold whitespace-nowrap myfontdesign dark:text-white">Artho</span>
            </a>
            <ul className="flex flex-wrap items-center mb-6 text-sm font-medium text-gray-500 sm:mb-0 dark:text-gray-400">
                <li>
                    <a href="#" className="hover:underline me-4 md:me-6">About</a>
                </li>
                <li>
                    <a href="#" className="hover:underline me-4 md:me-6">Privacy Policy</a>
                </li>
                <li>
                    <a href="#" className="hover:underline me-4 md:me-6">Contact</a>
                </li>
                <li>
                    <a href="#" className="hover:underline">Report</a>
                </li>
            </ul>
        </div>
        <hr className="my-6 border-gray-200 sm:mx-auto dark:border-gray-700 lg:my-8" />
        <span className="block text-sm text-gray-500 sm:text-center dark:text-gray-400">© 2025 <a href="https://flowbite.com/" className="hover:underline myfontdesign">Artho™</a>. All Rights Reserved.</span>
    </div>
</footer>

 
    </div>
  )
}

export default Footer
