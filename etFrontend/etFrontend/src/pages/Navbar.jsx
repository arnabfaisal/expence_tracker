// import React, { useState, useEffect } from "react";
// import { Button } from "@/components/ui/button";
// import { useNavigate, useLocation } from "react-router-dom";
// import {toast} from "sonner";

// import {
//   Dialog,
//   DialogContent,
//   DialogDescription,
//   DialogHeader,
//   DialogTitle,
//   DialogTrigger,
// } from "@/components/ui/dialog";

// function Navbar() {
//   const [isDialogOpen, setIsDialogOpen] = useState(false);
//   const [isAuthenticated, setIsAuthenticated] = useState(false);
//   const [email, setEmail] = useState("");
//   const navigate = useNavigate();
//   const location = useLocation();

//   useEffect(() => {
//     // Check for access token
//     const token = localStorage.getItem("access");

//     if (token) {
//       setIsAuthenticated(true);

//       // Simulated fetch from /api/user/me endpoint (replace with your API)
//       fetchUserProfile(token);
//     }
//   }, [location]);

//   const fetchUserProfile = async () => {
//     const token = localStorage.getItem("access");
//     const refresh = localStorage.getItem("refresh");
//     try {
//       const res = await fetch("http://127.0.0.1:8000/api/me/", {
//         headers: {
//           Authorization: `Bearer ${token}`,
//         },
//       });

//       if (!res.ok) throw new Error("Failed to fetch user");

//       const data = await res.json();
//       console.log("User profile data:", data); // ✅ move this above setEmail
//       setEmail(data.email);

//     } catch (err) {

//       setIsAuthenticated(false);
//       setEmail(null);
//     }
//   };

//   const [formData, setFormData] = useState({
//     email: "",
//     password: "",
//   });
//   const handleChange = (event) => {
//     const { name, value } = event.target;
//     setFormData((prev) => ({
//       ...prev,
//       [name]: value,
//     }));
//     console.log(name, value);
//   };

//   const handleSubmit = async (event) => {
//     event.preventDefault();
//     console.log(formData);

//     try {
//       const response = await fetch("http://127.0.0.1:8000/api/login/", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify(formData),
//       });

//       if (!response.ok) {
//         throw new Error("Login failed");
//       }

//       const data = await response.json();

//       // Example response: { access: "...", refresh: "..." }
//       localStorage.setItem("access", data.access);
//       localStorage.setItem("refresh", data.refresh);
//       await fetchUserProfile();
//       setIsAuthenticated(true);
//       setIsDialogOpen(false);
//       toast.success("Successfully logged in");
//       navigate("/dashboard");
//     } catch (error) {
//       toast.error("login failed");
//     }

//     setFormData({
//       email: "",
//       password: "",
//     });
//   };

//   const handleLogout = async () => {
//     const token = localStorage.getItem("access");
//     const refresh = localStorage.getItem("refresh");

//     try {
//       await fetch("http://127.0.0.1:8000/api/logout/", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//           Authorization: `Bearer ${token}`,
//         },
//         body: JSON.stringify({ refresh_token: refresh }),

//       });
//       toast.success("succesfully log out");
//     } catch (error) {
//       toast.error("failed to log out!")
//       // Even if logout fails, proceed to clear local storage
//     }

//     localStorage.removeItem("access");
//     localStorage.removeItem("refresh");
//     setIsAuthenticated(false);
//     setEmail(null); // or setUser(null) if you're storing the full user
//     navigate("/");
//   };

//   return (
//     <div className="container max-w-6xl mx-auto px-4">
//       <section className="">
//         <nav className="flex justify-between items-center h-25 px-4 sm:px-6 ">
//           <div>
//             <h1
//               className="logo cursor-pointer"
//               onClick={() => {
//                 navigate("/dashboard");
//               }}
//             >
//               ARTHO
//             </h1>
//           </div>
//           <div>
//             {!isAuthenticated ? (
//               <div>
//                 <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
//                   <DialogTrigger asChild>
//                     <Button onClick={() => setIsDialogOpen(true)}>Login</Button>
//                   </DialogTrigger>
//                   <DialogContent className="mydivdesign">
//                     <DialogHeader>
//                       <DialogTitle className="text-center text-xl">
//                         Login
//                       </DialogTitle>
//                       <DialogDescription className="text-center">
//                         Artho
//                       </DialogDescription>
//                     </DialogHeader>
//                     <form
//                       onSubmit={handleSubmit}
//                       className="flex flex-col md:gap-4 md:mt-4 md:px-30"
//                     >
//                       <div className="flex flex-col">
//                         <label
//                           htmlFor="email"
//                           className="mb-1 font-medium myfamily text-gray-800"
//                         >
//                           Email
//                         </label>
//                         <input
//                           id="email"
//                           type="text"
//                           placeholder="enter your email"
//                           className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
//                           onChange={handleChange}
//                           name="email"
//                           value={formData.email}
//                         />
//                       </div>
//                       <div className="flex flex-col">
//                         <label
//                           htmlFor="password"
//                           className="mb-1 font-medium myfamily text-gray-800"
//                         >
//                           Password
//                         </label>
//                         <input
//                           id="password"
//                           type="password"
//                           placeholder="enter your password"
//                           className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
//                           name="password"
//                           value={formData.password}
//                           onChange={handleChange}
//                         />
//                       </div>
//                       <div>
//                         <Button type="submit" className="w-full mt-3">
//                           login
//                         </Button>
//                       </div>
//                     </form>
//                   </DialogContent>
//                 </Dialog>
//               </div>
//             ) : (
//               <div className="flex gap-5 items-center">
//                 <p>{email}</p>
//                 <div>
//                   <Button onClick={handleLogout}>logout</Button>
//                 </div>
//               </div>
//             )}
//           </div>
//         </nav>
//       </section>
//       <section></section>
//     </div>
//   );
// }

// export default Navbar;











import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { useNavigate, useLocation } from "react-router-dom";
import { toast } from "sonner";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from "@/components/ui/popover";

function Navbar() {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const token = localStorage.getItem("access");

    if (token) {
      setIsAuthenticated(true);
      fetchUserProfile(token);
    }
  }, [location]);

  const fetchUserProfile = async () => {
    const token = localStorage.getItem("access");
    try {
      const res = await fetch("http://127.0.0.1:8000/api/me/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error("Failed to fetch user");

      const data = await res.json();
      setUserData(data);
    } catch (err) {
      setIsAuthenticated(false);
      setUserData(null);
    }
  };

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      const data = await response.json();
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      await fetchUserProfile();
      setIsAuthenticated(true);
      setIsDialogOpen(false);
      toast.success("Successfully logged in");
      navigate("/dashboard");
    } catch (error) {
      toast.error("Login failed");
    }

    setFormData({ email: "", password: "" });
  };

  const handleLogout = async () => {
    const token = localStorage.getItem("access");
    const refresh = localStorage.getItem("refresh");

    try {
      await fetch("http://127.0.0.1:8000/api/logout/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ refresh_token: refresh }),
      });

      toast.success("Successfully logged out");
    } catch (error) {
      toast.error("Failed to log out");
    }

    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setIsAuthenticated(false);
    setUserData(null);
    navigate("/");
  };

  return (
    <div className="container max-w-6xl mx-auto px-4">
      <nav className="flex justify-between items-center h-25 px-4 sm:px-6">
        <h1
          className="logo cursor-pointer"
          onClick={() => navigate("/dashboard")}
        >
          ARTHO
        </h1>

        {!isAuthenticated ? (
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={() => setIsDialogOpen(true)}>Login</Button>
            </DialogTrigger>
            <DialogContent className="mydivdesign">
              <DialogHeader>
                <DialogTitle className="text-center text-xl">Login</DialogTitle>
                <DialogDescription className="text-center">Artho</DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="flex flex-col md:gap-4 md:mt-4">
                <div className="flex flex-col">
                  <label htmlFor="email" className="mb-1 font-medium myfamily text-gray-800">
                    Email
                  </label>
                  <input
                    id="email"
                    type="text"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Enter your email"
                    className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 bg-gray-100 focus:outline-none focus:ring-mycolor"
                  />
                </div>
                <div className="flex flex-col">
                  <label htmlFor="password" className="mb-1 font-medium myfamily text-gray-800">
                    Password
                  </label>
                  <input
                    id="password"
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Enter your password"
                    className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 bg-gray-100 focus:outline-none focus:ring-mycolor"
                  />
                </div>
                <Button type="submit" className="w-full mt-3">Login</Button>
              </form>
            </DialogContent>
          </Dialog>
        ) : (
          <div className="flex gap-5 items-center">
            <Popover>
              <PopoverTrigger asChild>
                <div className="flex items-center gap-2 cursor-pointer">
                  <div className="w-8 h-8 bg-maati rounded-full flex items-center justify-center text-white uppercase font-semibold">
                    {userData?.email?.[0]}
                  </div>
                  <span className="text-sm">{userData?.email}</span>
                </div>
              </PopoverTrigger>
              <PopoverContent className="w-64 space-y-2 text-sm">
                <div>
                  <p><strong>Name:</strong> {`${userData?.first_name} ${userData?.last_name} ` || "N/A"}</p>
                  <p><strong>Email:</strong> {userData?.email}</p>
                </div>
                <Button className="bg-laal" size="sm" onClick={handleLogout}>
                  Logout
                </Button>
              </PopoverContent>
            </Popover>
          </div>
        )}
      </nav>
    </div>
  );
}

export default Navbar;
