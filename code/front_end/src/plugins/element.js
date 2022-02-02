import Vue from 'vue'
import{
    Message,
    Radio,
    RadioGroup,
    Notification,
    Icon,
    Button,
    Dialog,
    Popover,
    MessageBox,
}from 'element-ui';

Vue.prototype.$message = Message;
Vue.use(Radio);
Vue.use(RadioGroup);
Vue.use(Icon);
Vue.use(Button);
Vue.use(Dialog);
Vue.use(Popover);
Vue.prototype.$notify = Notification;
Vue.prototype.$confirm = MessageBox.confirm;