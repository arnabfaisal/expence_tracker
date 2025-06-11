import React ,{useState , useEffect} from "react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { toast } from 'sonner';
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
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Check for access token
    const token = localStorage.getItem("access");

    if (token) {
      setIsAuthenticated(true);

      // Simulated fetch from /api/user/me endpoint (replace with your API)
      fetchUserProfile();
    }
  }, []);

  const fetchUserProfile = async () => {
    const token = localStorage.getItem("access");
    const refresh = localStorage.getItem("refresh");
    try {
      const res = await fetch("http://127.0.0.1:8000/api/me/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error("Failed to fetch user");

      const data = await res.json();
      console.log("User profile data:", data); // ✅ move this above setEmail
      setEmail(data.email);
      toast.success("Registration Successful");
    } catch (err) {
      toast.error("Registration Failed");
      setIsAuthenticated(false);
      setEmail(null);
    }
  };

  const [formData, setFormData] = useState({
    email: "",
    password: "",
    password2: "",
    first_name: "",
    last_name: "",
  });
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    console.log(name, value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(formData);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        throw new Error("Registration failed");
      }



      const formData2 = {
        "email": formData['email'],
        "password": formData['password'],
      }
      const response = await fetch("http://127.0.0.1:8000/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData2),
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      const data = await response.json();

      // Example response: { access: "...", refresh: "..." }
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      await fetchUserProfile();
      setIsAuthenticated(true);
      setIsDialogOpen(false);
      navigate("/dashboard");
    } catch (error) {
      console.error("Login error:", error.message);
    }

    setFormData({
      email: "",
      password: "",
      password2: "",
      first_name: "",
      last_name: "",
    });
  };

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
                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                  <DialogTrigger asChild>
                    <Button className="lg" onClick={() => setIsDialogOpen(true)}>Join now</Button>
                  </DialogTrigger>
                  <DialogContent className="mydivdesign">
                    <DialogHeader>
                      <DialogTitle className="text-center text-2xl">
                        Register
                      </DialogTitle>
                      <DialogDescription className="text-center">
                        Artho
                      </DialogDescription>
                    </DialogHeader>
                    <form
                      onSubmit={handleSubmit}
                      className="flex flex-col md:gap-4 md:mt-4 md:px-30"
                    >
                      <div className="flex flex-col">
                        <label
                          htmlFor="email"
                          className="mb-1 font-medium myfamily text-gray-800"
                        >
                          Email
                        </label>
                        <input
                          id="email"
                          type="text"
                          placeholder="enter your email"
                          className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                          onChange={handleChange}
                          name="email"
                          value={formData.email}
                          required
                        />
                      </div>
                      <div className="flex flex-col">
                        <label
                          htmlFor="password"
                          className="mb-1 font-medium myfamily text-gray-800"
                        >
                          Password
                        </label>
                        <input
                          id="password"
                          type="password"
                          placeholder="enter your password"
                          className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                          name="password"
                          value={formData.password}
                          onChange={handleChange}
                          required
                        /> 
                      </div>
                      <div className="flex flex-col">
                        <label
                          htmlFor="password2"
                          className="mb-1 font-medium myfamily text-gray-800"
                        >
                          Password Again
                        </label>
                        <input
                          id="password2"
                          type="password"
                          placeholder="password again"
                          className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                          name="password2"
                          value={formData.password2}
                          onChange={handleChange}
                          required
                        />
                      </div>
                      <div className="flex flex-col">
                        <label
                          htmlFor="firstname"
                          className="mb-1 font-medium myfamily text-gray-800"
                        >
                          First name
                        </label>
                        <input
                          id="firstname"
                          type="text"
                          placeholder="first name"
                          className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                          name="first_name"
                          value={formData.first_name}
                          onChange={handleChange}
                          required
                        />
                      </div>
                      <div className="flex flex-col">
                        <label
                          htmlFor="lastname"
                          className="mb-1 font-medium myfamily text-gray-800"
                        >
                          Last name
                        </label>
                        <input
                          id="lastname"
                          type="text"
                          placeholder="last name"
                          className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                          name="last_name"
                          value={formData.last_name}
                          onChange={handleChange}
                          required
                        />
                      </div>
                      <div>
                        <Button type="submit" className="w-full mt-3">
                          Register
                        </Button>
                      </div>
                    </form>
                  </DialogContent>
                </Dialog>
              </div>
            </div>
          </div>
        </motion.div>
        <div className="hidden md:block w-full flex-1">
          <div className="bg-white h-[500px] rounded-2xl overflow-hidden shadow-lg shadow-mycolor flex items-center justify-center mx-auto">
            <img
              src="./src/assets/charts.png"
              alt="chart"
              className="w-full h-full object-cover p-4"
            />
          </div>
        </div>
      </section>

      <section className="sneakpeak mt-5 flex flex-col md:flex-row md:mt-50 md:justify-between gap-10 items-center">
        <div className="flex-1 w-full">
          <div className="bg-white h-[500px] rounded-2xl overflow-hidden shadow-lg shadow-mycolor flex items-center justify-center mx-auto">
            <img
              src="./src/assets/goal.png"
              alt="goal"
              className="w-full h-full object-cover p-4"
            />
          </div>
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
              Every transaction brings you closer and view your full history
              once a <span className="myfontdesign">goal</span> is complete.
            </h1>
          </div>
        </motion.div>
      </section>
    </div>
  );
}

export default Landingpage;
