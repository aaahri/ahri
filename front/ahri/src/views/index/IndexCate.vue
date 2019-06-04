<template>
  <div id="indexcate" class="indexcate">
    <p v-for="i in category" @click="goto(i.first)">{{i.name}}&nbsp;&nbsp;</p>
  </div>
</template>

<script>
import msg from "@/assets/tips";
import loading from "@/assets/loading";
import url from "@/assets/server";
import Qs from "qs";
export default {
  name: "indexcate",
  data() {
    return {
      category: []
    };
  },
  methods: {
    goto(id) {
      if (id !== "")
        this.$router.push({ path: "/read", query: { id: id.$oid } });
    }
  },
  mounted() {
    let load = loading(document.getElementById("indexcate"));
    let self = this;
    this.axios
      .get(url + "/api/index/indexcate")
      .then(response => {
        if (response.data.code === 200) {
          self.category = JSON.parse(response.data.data);
          document.getElementById("indexcate").removeChild(load);
        } else {
          msg("未知错误..(from category get 500)", "#FF9966");
          console.log(response.data);
        }
      })
      .catch(response => {
        msg("未知错误..", "#FF9966");
        console.log(response);
      });
  }
};
</script>

<style lang="scss" scoped>
.indexcate {
  position: relative;
  padding: 15px;
  display: flex;
  flex-wrap: wrap;
  min-height: 30px;
  p {
    margin: 0 15px;
    color: #777;
    font-weight: 700;
    transition: 0.4s;
    cursor: pointer;
    text-decoration: underline;
    &:hover {
      color: #333;
      text-decoration: none;
    }
    &:active {
      color: #000;
    }
  }
}
</style>
