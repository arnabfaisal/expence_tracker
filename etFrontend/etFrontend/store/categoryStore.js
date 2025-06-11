import { create } from 'zustand'

// const useStore = create((set) => ({
//   count: 1,
//   inc: () => set((state) => ({ count: state.count + 1 })),
// }))

// function Counter() {
//   const { count, inc } = useStore()
//   return (
//     <div>
//       <span>{count}</span>
//       <button onClick={inc}>one up</button>
//     </div>
//   )
// }


export const useCategoryStore = create((set) => ({
  categories: [],
  loading: false,
  error: null,

  fetchCategories: async () => {
    set({loading: true, error: null});
    const token = localStorage.getItem("access");

    try {
      const response = await fetch("http://127.0.0.1:8000/api/global/", {
        headers: {
          "Content-Type": "application/json",
        }
      });
      const data = await response.json();
      set({categories: [...data],loading:false})
      
    } catch (error) {
      error: "failed to load Balances";
      loading: false;
      
    }
  }

}))