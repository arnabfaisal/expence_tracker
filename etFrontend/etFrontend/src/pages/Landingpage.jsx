import React from "react";
import {Button} from '@/components/ui/button'
function Landingpage() {
  return (
    <div className="container mx-auto px-4 sm:px-6 mt-10">
      <section className="hero flex flex-col items-center">
        <div>
          <h1 className="text-4xl text-center sm:text-4xl max-w-xl mx-auto">
            For  managing your <span className="myfontdesign">expense</span> and tracking your <span className="myfontdesign">goals</span> with ease
          </h1>
        </div>

        <div className="mt-10">
          <Button className="lg">Join now</Button>
        </div>
      </section>



      <section className="sneakpeak mt-5">
        <div className="bg-amber-100 h-[500px]">
        </div>
      </section>
    </div>
  );
}

export default Landingpage;
