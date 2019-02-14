<template>
  <div class="CheckBox" id="checkbox-div-{{item.id}}">
    <input
      id="checkbox-{{item.id}}"
      key="checkbox-key-{{item.id}}"
      type="checkbox"
      value="{{item.value}}"
      checked="{{checked}}"
      onChange="{{toggleCheckboxChange}}"
    >
    <span key="checkbox-label-{{item.id}}" class="{{getClassByParticipantTypeName(item.name)}}"/>
    - {item.label}
  </div>
</template>

<script>
export default {
  name: "dtp-checkbox",
  props: {
    item: {
      id: Number,
      value: Boolean,
      name: String,
      label: String
    },
    handleCheckboxChange: Function
  },
  data() {
    return {
      checked: Boolean
    };
  },
  methods: {
    toggleCheckboxChange() {
      const handleCheckboxChange = this.handleCheckboxChange;

      let checkedByUser = !this.checked;
      let new_item = this.item;
      new_item.value = checkedByUser;
      handleCheckboxChange(new_item);
    }
  }
};
</script>
