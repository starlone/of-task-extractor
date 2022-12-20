const { createApp } = Vue;

createApp({
  data() {
    return {
      project: "/kdi_nia/git/*",
      tasks: [{ name: "feat" }],
      response: {
        tasks: [
          {
            files: [],
            commits: [],
            task: "-",
          },
        ],
      },
    };
  },
  methods: {
    onChange() {
      // Split by space
      let tasks = this.tasks
        .map((item) => item.name)
        .filter((item) => item)
        .map((item) => item.trim())
        .map((item) => item.split(" "));

      // Concat array to payload
      tasks = [].concat(...tasks);

      // Update
      this.tasks = tasks.map((item) => {
        return {
          name: item,
        };
      });
    },
    onSubmit() {
      const payload = {
        project: this.project,
        tasks: this.tasks.map((item) => item.name),
      };
      axios.post("/api", payload).then((response) => {
        this.response = response.data;
      });
    },
    addTask() {
      this.tasks.push({ name: "" });
    },
    removeTask(item) {
      const pos = this.tasks.indexOf(item);
      if (pos != -1) {
        this.tasks.splice(pos, 1);
      }
    },
  },
}).mount("#app");
