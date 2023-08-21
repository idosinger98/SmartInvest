/**
 * this Notification
 * 
 * Is a simple notification system that can be used to display notifications for your own app.
 * 
 * Version: 1.1.0
 * Author: Skyyinfinity
 * Author URL: https://github.com/SkyyInfinity
 * License: MIT
 */

export function sendToastMessage(message, type, options = {}){
    const defaultOptions = {
        title: "",
        autoClose: 5000,
        container: document.body,
    };

    const { title, autoClose, container } = { ...defaultOptions, ...options };

    Toastinette.init({
            position: 'top-center',
            title: title,
            message: message,
            type: type,
            autoClose: autoClose,
            progress: true
    }, container);
}

export const MESSAGE_TYPE = Object.freeze({
    SUCCESS: 'success',
    ERROR: 'error',
    INFO: 'info',
    WARNING: 'warning',
})

const Toastinette = {

    C_INFO: 'var(--toastInette-info)',
    C_WARNING: 'var(--toastInette-warning)',
    C_ERROR: 'var(--toastInette-error)',
    C_SUCCESS: 'var(--toastInette-success)',

    init(options, container) {
        let toastInette = this.create(options.position, options.title, options.message, options.type)
        container.appendChild(toastInette);

        let close = document.querySelectorAll('.toastInette-close button');

        // close toastInette on click on close button
        if(close.length > 0) {
            close.forEach((btn) => {
                btn.addEventListener('click', () => {
                    this.removeToast(toastInette);
                });
            });
        }

        // else close toastInette after duration
        if(!isNaN(options.autoClose) && (options.autoClose !== false) && (options.autoClose !== undefined)) {
            if(options.progress === true) {
                // Animate the progress bar
                toastInette.classList.add('toastInette-auto-close');
                this.animateProgressBar(toastInette, options.autoClose, options.progress);
            }

            // Close toastInette after duration
            setTimeout(() => {
                this.removeToast(toastInette);
            }, options.autoClose);
        }
    },

    create(position = 'top-center', title, message = 'message', type = 'success') {
        // Variables
        let 
        progress,
        toastInette,
        toastIcon,
        toastContent,
        toastTitle,
        toastMessage,
        toastClose,
        toastCloseButton;

        // Generate toastInette Progress Bar
        progress = this.generateProgressBar();

        // Generate toastInette
        toastInette = this.generateToast(type, position);

        // Generate toastInette Icon
        toastIcon = this.generateToastIcon(type);

        // Generate toastInette Content
        toastContent = this.generateToastContent(title, message).toastContent;
        toastTitle = this.generateToastContent(title, message).toastTitle;
        toastMessage = this.generateToastContent(title, message).toastMessage;

        // Generate toastInette Close Button
        toastClose = this.generateCloseBtn(type).toastClose;
        toastCloseButton = this.generateCloseBtn(type).toastCloseButton;

        // Append Elements
        toastClose.appendChild(toastCloseButton);
        if(title !== undefined && title !== '') {
            toastContent.appendChild(toastTitle);
        }
        toastContent.appendChild(toastMessage);
        toastInette.appendChild(toastIcon);
        toastInette.appendChild(toastContent);
        toastInette.appendChild(toastClose);
        toastInette.appendChild(progress);
        
        return toastInette;
    },

    generateProgressBar() {
        let progress;

        progress = document.createElement('div');
        progress.classList.add('toastInette-progress');

        return progress;
    },

    generateToast(type, position) {
        let toastInette;

        toastInette = document.createElement('div');
        toastInette.classList.add('toastInette');
        
        switch(type) {
            case 'success':
                toastInette.classList.add('toastInette-success');
                break;
            case 'error':
                toastInette.classList.add('toastInette-error');
                break;
            case 'warning':
                toastInette.classList.add('toastInette-warning');
                break;
            case 'info':
                toastInette.classList.add('toastInette-info');
                break;
        }
        toastInette.dataset.position = position;

        return toastInette;
    },

    generateToastIcon(type) {
        let toastIcon;

        toastIcon = document.createElement('div');
        toastIcon.classList.add('toastInette-icon');
        switch(type) {
            case 'success':
                toastIcon.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\"><path fill=\"none\" d=\"M0 0h24v24H0z\"/><path d=\"M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16zm-.997-4L6.76 11.757l1.414-1.414 2.829 2.829 5.656-5.657 1.415 1.414L11.003 16z\" fill=\"" + this.C_SUCCESS + "\"/></svg>";
                break;
            case 'error':
                toastIcon.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\"><path fill=\"none\" d=\"M0 0h24v24H0z\"/><path d=\"M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16zm-1-5h2v2h-2v-2zm0-8h2v6h-2V7z\" fill=\"" + this.C_ERROR + "\"/></svg>";
                break;
            case 'warning':
                toastIcon.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\"><path fill=\"none\" d=\"M0 0h24v24H0z\"/><path d=\"M12.866 3l9.526 16.5a1 1 0 0 1-.866 1.5H2.474a1 1 0 0 1-.866-1.5L11.134 3a1 1 0 0 1 1.732 0zm-8.66 16h15.588L12 5.5 4.206 19zM11 16h2v2h-2v-2zm0-7h2v5h-2V9z\" fill=\"" + this.C_WARNING + "\"/></svg>";
                break;
            case 'info':
                toastIcon.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\"><path fill=\"none\" d=\"M0 0h24v24H0z\"/><path d=\"M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM11 7h2v2h-2V7zm0 4h2v6h-2v-6z\" fill=\"" + this.C_INFO + "\"/></svg>";
                break;
        }

        return toastIcon;
    },

    generateToastContent(title, message) {
        let 
        toastContent, 
        toastTitle, 
        toastMessage;

        toastContent = document.createElement('div');
        toastContent.classList.add('toastInette-content');

        // toastInette Title
        if(title !== undefined && title !== '') {
            toastTitle = document.createElement('div');
            toastTitle.classList.add('toastInette-title');
            toastTitle.innerText = title;
        }

        // toastInette Message
        toastMessage = document.createElement('div');
        toastMessage.classList.add('toastInette-message');
        toastMessage.innerText = message;

        return { toastContent, toastTitle, toastMessage };
    },

    generateCloseBtn(type) {
        let 
        toastClose, 
        toastCloseButton;

        toastClose = document.createElement('div');
        toastClose.classList.add('toastInette-close');

        // toastInette Close Button
        toastCloseButton = document.createElement('button');
        switch(type) {
            case 'success':
                toastCloseButton.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\"><path fill=\"none\" d=\"M0 0h24v24H0z\"/><path d=\"M12 10.586l4.95-4.95 1.414 1.414-4.95 4.95 4.95 4.95-1.414 1.414-4.95-4.95-4.95 4.95-1.414-1.414 4.95-4.95-4.95-4.95L7.05 5.636z\" fill=\"" + this.C_SUCCESS + "\"/></svg>";
                break;
            case 'error':
                toastCloseButton.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\"><path fill=\"none\" d=\"M0 0h24v24H0z\"/><path d=\"M12 10.586l4.95-4.95 1.414 1.414-4.95 4.95 4.95 4.95-1.414 1.414-4.95-4.95-4.95 4.95-1.414-1.414 4.95-4.95-4.95-4.95L7.05 5.636z\" fill=\"" + this.C_ERROR + "\"/></svg>";
                break;
            case 'warning':
                toastCloseButton.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\"><path fill=\"none\" d=\"M0 0h24v24H0z\"/><path d=\"M12 10.586l4.95-4.95 1.414 1.414-4.95 4.95 4.95 4.95-1.414 1.414-4.95-4.95-4.95 4.95-1.414-1.414 4.95-4.95-4.95-4.95L7.05 5.636z\" fill=\"" + this.C_WARNING + "\"/></svg>";
                break;
            case 'info':
                toastCloseButton.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\"><path fill=\"none\" d=\"M0 0h24v24H0z\"/><path d=\"M12 10.586l4.95-4.95 1.414 1.414-4.95 4.95 4.95 4.95-1.414 1.414-4.95-4.95-4.95 4.95-1.414-1.414 4.95-4.95-4.95-4.95L7.05 5.636z\" fill=\"" + this.C_INFO + "\"/></svg>";
                break;
        }

        return { toastClose, toastCloseButton };
    },

    removeToast(toastInette) {
        const DELETION_DURATION = 600;

        toastInette.style.animation = `toastFadeOut ${DELETION_DURATION}ms ease-out backwards`;
        setTimeout(() => {
            toastInette.remove();
        }, DELETION_DURATION);
    },

    animateProgressBar(toastInette, duration, progress) {
        let progressBar = toastInette.querySelector('.toastInette-progress');

        if(progress === true) {
            progressBar.style.animation = `progressBar ${duration}ms ease-in-out forwards`;
        }
    }
}