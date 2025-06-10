import React from "react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

// <Button>Click me</Button>

function Landingpage() {
  return (
    <div className="container max-w-6xl mx-auto px-4 sm:px-6 mt-10 min-h-screen">
      <section className="hero flex flex-col md:flex-row items-center md:justify-between">
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          whileInView={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          viewport={{ once: true }}
          className="flex flex-1 flex-col items-center"
        >
          <div className="flex flex-1 flex-col items-center">
            <div>
              <h1 className="text-4xl text-center sm:text-4xl md:text-4xl max-w-xl mx-auto font-myfamily">
                For managing your <span className="myfontdesign">expense</span>{" "}
                and tracking your <span className="myfontdesign">goals</span>{" "}
                with ease
              </h1>
            </div>

            <div className="mt-10">
              <div>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button className="lg">Join now</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Are you absolutely sure?</DialogTitle>
                      <DialogDescription>
                        This action cannot be undone. This will permanently
                        delete your account and remove your data from our
                        servers.
                      </DialogDescription>
                    </DialogHeader>
                  </DialogContent>
                </Dialog>
              </div>
            </div>
          </div>
        </motion.div>
        <div className="hidden md:block w-full flex-1">
          <div className="bg-white h-[500px] rounded-2xl overflow-hidden shadow-lg shadow-mycolor flex items-center justify-center mx-auto">
            <img src="./src/assets/charts.png" alt="chart" className="w-full h-full object-cover p-4"/>
          </div>
        </div>
      </section>

      <section className="sneakpeak mt-5 flex flex-col md:flex-row md:mt-20 md:justify-between gap-10 items-center">
        <div className="flex-1 w-full">
          <div className="bg-amber-100 h-[500px]"></div>
        </div>

        <motion.div
          initial={{ opacity: 0, x: 50 }}
          whileInView={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          viewport={{ once: true }}
          className="hidden md:block w-full flex-1"
        >
          <div className="hidden md:block w-full flex-1">
            <h1 className="md: text-3xl font-myfamily">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Libero
              velit obcaecati consequuntur dolore provident inventore aspernatur
              dolorum quod accusantium, impedit esse nulla animi magnam. In
              soluta
            </h1>
          </div>
        </motion.div>
      </section>
    </div>
  );
}

export default Landingpage;
