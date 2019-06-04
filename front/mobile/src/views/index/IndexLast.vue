<template>
  <div id="indexlast" class="indexlast">
    <p v-for="i in category" @click="goto(i._id)">
      <span class="title">{{i.title}}</span>
    </p>
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
      this.$router.push({ path: "/read", query: { id: id.$oid } });
    }
  },
  mounted() {
    let load = loading(document.getElementById("indexlast"));
    let self = this;
    this.axios
      .get(url + "/api/index/indexlast")
      .then(response => {
        if (response.data.code === 200) {
          self.category = JSON.parse(response.data.data);
          document.getElementById("indexlast").removeChild(load);
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
.indexlast {
  position: relative;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 30px;
  p {
    margin: 5px 15px;
    color: #777;
    font-weight: 700;
    cursor: pointer;
    text-decoration: underline;
    &:active {
      color: #000;
    }
    .title {
      width: 0;
      text-align: right;
      text-decoration: underline;
    }
  }
}
</style>
