const { createApp } = Vue;

createApp({
  data() {
    let config = {
      project: "/home/user/git/*",
      tasks: [{ name: "feat" }],
      submited: false,
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
    axios
      .get("/config")
      .then((response) => this.project = response.data.projects_path)
      .catch((error) => alert(error));
    return config;
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
      this.submited = true;
      const payload = {
        project: this.project,
        tasks: this.tasks.map((item) => item.name),
      };
      axios
        .post("/api", payload)
        .then((response) => {
          this.response = response.data;
        })
        .catch((error) => {
          alert(error);
        })
        .then(() => {
          this.submited = false;
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
