import React from "react";
import { Button } from "@/components/ui/button";
function Landingpage() {
  return (
    <div className="container max-w-6xl mx-auto px-4 sm:px-6 mt-10">
      <section className="hero flex flex-col md:flex-row items-center md:justify-between">
        <div className="flex flex-1 flex-col items-center">
          <div>
            <h1 className="text-4xl text-center sm:text-4xl md:text-4xl max-w-xl mx-auto font-myfamily">
              For managing your <span className="myfontdesign">expense</span>{" "}
              and tracking your <span className="myfontdesign">goals</span> with
              ease
            </h1>
          </div>

          <div className="mt-10">
            <Button className="lg">Join now</Button>
          </div>
        </div>
        <div className="hidden md:block w-full flex-1">
          <div className="bg-amber-100 h-[500px] rounded-4xl"></div>
        </div>
      </section>

      <section className="sneakpeak mt-5 flex flex-col md:flex-row md:mt-20 md:justify-between gap-10 items-center">
        <div className="flex-1 w-full">
        <div className="bg-amber-100 h-[500px]"></div>
        </div>
        <div className="hidden md:block w-full flex-1">
          <h1 className="md: text-3xl font-myfamily">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Libero
            velit obcaecati consequuntur dolore provident inventore aspernatur
            dolorum quod accusantium, impedit esse nulla animi magnam. In
            soluta
          </h1>
        </div>
      </section>
    </div>
  );
}

export default Landingpage;
