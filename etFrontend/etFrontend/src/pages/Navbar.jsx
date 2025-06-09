import React from "react";
import {Button} from '@/components/ui/button'
function Navbar() {
  return (
    <div className="container max-w-6xl mx-auto px-4">
      <section className="">
        <nav className="flex justify-between items-center h-25 px-4 sm:px-6 ">
          <div>
            <h1 className="logo">ARTHO</h1>
          </div>
          <div>
            <Button>login</Button>
          </div>
        </nav>
      </section>
      <section>

      </section>
    </div>
  );
}

export default Navbar;